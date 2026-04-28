// import { Kafka } from "kafkajs";

// const KAFKA_BROKERS = process.env.KAFKA_BROKERS || "localhost:9092";

// const kafka = new Kafka({
//   clientId: "nepal-pulse-ingestion",
//   brokers: KAFKA_BROKERS.split(","),
// });

// const producer = kafka.producer();

// async function run() {
//   try {
//     await producer.connect();

//     const message = {
//       source: "test-node-service",
//       title: "नेपाल समाचार परीक्षण",
//       summary:
//         "This is the first message sent from the Node.js ingestion service.",
//       language: "ne",
//       category: "general",
//       url: "https://example.com/test-news",
//       scraped_at: new Date().toISOString(),
//     };

//     await producer.send({
//       topic: "raw-news",
//       messages: [
//         {
//           value: JSON.stringify(message),
//         },
//       ],
//     });

//     console.log("✅ Message sent to Kafka topic raw-news");
//     console.log(message);
//   } catch (error) {
//     console.error("❌ Error sending message:", error);
//   } finally {
//     await producer.disconnect();
//   }
// }

// run();

import axios from "axios";
import * as cheerio from "cheerio";
import { Kafka } from "kafkajs";

type NewsItem = {
  source: string;
  title: string;
  summary: string;
  language: string;
  category: string;
  url: string;
  scraped_at: string;
};

type SourceConfig = {
  name: string;
  url: string;
  lang: string;
};

const KAFKA_BROKERS = process.env.KAFKA_BROKERS || "localhost:9092";
const SCRAPE_INTERVAL = parseInt(process.env.SCRAPE_INTERVAL || "3600000"); // 1 hour

const kafka = new Kafka({
  clientId: "nepal-pulse-ingestion",
  brokers: KAFKA_BROKERS.split(","),
});

const producer = kafka.producer();

const sources: SourceConfig[] = [
  { name: "Kathmandu Post", url: "https://kathmandupost.com", lang: "en" },
  { name: "OnlineKhabar", url: "https://english.onlinekhabar.com", lang: "en" },
  { name: "Setopati", url: "https://www.setopati.com", lang: "ne" },
  { name: "Ratopati", url: "https://www.ratopati.com", lang: "ne" },
  {
    name: "Nagarik",
    url: "https://nagariknews.nagariknetwork.com",
    lang: "ne",
  },
  { name: "Annapurna Post", url: "https://annapurnapost.com", lang: "ne" },
  { name: "Himalayan Times", url: "https://thehimalayantimes.com", lang: "en" },
  {
    name: "Republica",
    url: "https://myrepublica.nagariknetwork.com",
    lang: "en",
  },
  { name: "BBC Nepali", url: "https://www.bbc.com/nepali", lang: "ne" },
  { name: "Kantipur", url: "https://ekantipur.com", lang: "ne" },
  { name: "Desh Sanchar", url: "https://deshsanchar.com", lang: "ne" },
  { name: "Gorkhapatra", url: "https://gorkhapatraonline.com", lang: "ne" },
  { name: "Nepal News", url: "https://nepalnews.com", lang: "en" },
  { name: "Bizmandu", url: "https://bizmandu.com", lang: "ne" },
  { name: "ImageKhabar", url: "https://www.imagekhabar.com", lang: "ne" },
  { name: "Arthasarokar", url: "https://arthasarokar.com", lang: "ne" },
  { name: "Sajha Post", url: "https://sajhapost.com", lang: "ne" },
  {
    name: "Nepal Live Today",
    url: "https://www.nepallivetoday.com",
    lang: "en",
  },
  { name: "Online News Nepal", url: "https://onlinenewsnepal.com", lang: "ne" },
  { name: "Dainik Nepal", url: "https://dainiknepal.com", lang: "ne" },
];

function deduplicate(items: NewsItem[]): NewsItem[] {
  const seen = new Set<string>();
  return items.filter((item) => {
    const key = `${item.source}-${item.title}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function buildAbsoluteUrl(baseUrl: string, href: string): string {
  try {
    return new URL(href, baseUrl).href;
  } catch {
    return href;
  }
}

async function scrapeGeneric(source: SourceConfig): Promise<NewsItem[]> {
  try {
    const response = await axios.get(source.url, {
      timeout: 10000,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
      },
    });

    const $ = cheerio.load(response.data);
    const items: NewsItem[] = [];

    $("h1 a, h2 a, h3 a").each((_, el) => {
      const title = $(el).text().trim();
      const href = $(el).attr("href")?.trim();

      if (!title || !href) return;
      if (title.length < 20) return;

      items.push({
        source: source.name,
        title,
        summary: "",
        language: source.lang,
        category: "general",
        url: buildAbsoluteUrl(source.url, href),
        scraped_at: new Date().toISOString(),
      });
    });

    const cleaned = deduplicate(items).slice(0, 5);
    console.log(`✅ Scraped ${cleaned.length} items from ${source.name}`);
    return cleaned;
  } catch (error) {
    console.log(`❌ Failed: ${source.name}`);
    return [];
  }
}

async function publishNews(items: NewsItem[]) {
  for (const item of items) {
    await producer.send({
      topic: "raw-news",
      messages: [{ value: JSON.stringify(item) }],
    });
    console.log(`✅ Published: ${item.source} - ${item.title}`);
  }
}

async function scrapeAndPublish() {
  try {
    console.log(`\n🔄 Starting scrape at ${new Date().toISOString()}`);
    let allNews: NewsItem[] = [];

    for (const source of sources) {
      const news = await scrapeGeneric(source);
      allNews = [...allNews, ...news];
    }

    allNews = deduplicate(allNews);
    console.log(
      `\nFound ${allNews.length} total news items from ${sources.length} websites\n`,
    );

    if (allNews.length > 0) {
      await publishNews(allNews);
    } else {
      console.log("⚠️ No news items found in this scrape");
    }
  } catch (error) {
    console.error("❌ Scraper error:", error);
  }
}

async function run() {
  try {
    console.log(`🚀 Connecting to Kafka brokers: ${KAFKA_BROKERS}`);
    await producer.connect();
    console.log("✅ Connected to Kafka");

    // Run scraper immediately
    await scrapeAndPublish();

    // Then run at intervals
    setInterval(async () => {
      await scrapeAndPublish();
    }, SCRAPE_INTERVAL);

    console.log(
      `⏰ Service running. Will scrape every ${SCRAPE_INTERVAL / 1000 / 60} minutes`,
    );
  } catch (error) {
    console.error("❌ Fatal error:", error);
    process.exit(1);
  }
}

// Handle graceful shutdown
process.on("SIGTERM", async () => {
  console.log("SIGTERM received, disconnecting...");
  await producer.disconnect();
  process.exit(0);
});

process.on("SIGINT", async () => {
  console.log("SIGINT received, disconnecting...");
  await producer.disconnect();
  process.exit(0);
});

run();