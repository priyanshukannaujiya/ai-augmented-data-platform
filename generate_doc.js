const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, TableOfContents,
  Table, TableRow, TableCell, WidthType, ShadingType,
  AlignmentType, PageBreak
} = require("docx");
const fs = require("fs");

// ---------- helpers ----------
const H1 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_1, pageBreakBefore: true });
const H2 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });
const H3 = (text) => new Paragraph({ text, heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 100 } });
const P = (text) => new Paragraph({ children: [new TextRun({ text })], spacing: { after: 160 } });
const Note = (text) => new Paragraph({ children: [new TextRun({ text, italics: true, color: "555555" })], spacing: { after: 160 } });

function bulletList(items) {
  return items.map(t => new Paragraph({
    text: t,
    numbering: { reference: "bullet-list", level: 0 },
    spacing: { after: 60 }
  }));
}

function qa(q, a) {
  return [
    new Paragraph({
      children: [new TextRun({ text: "Q: ", bold: true }), new TextRun({ text: q, bold: true })],
      spacing: { before: 160, after: 60 }
    }),
    new Paragraph({
      children: [new TextRun({ text: "A: ", bold: true }), new TextRun({ text: a })],
      spacing: { after: 60 }
    })
  ];
}

function qaBlock(title, list) {
  const out = [H3(title)];
  list.forEach(([q, a]) => out.push(...qa(q, a)));
  return out;
}

function simpleTable(headers, rows, widths) {
  const totalWidth = 9000;
  const w = widths || headers.map(() => Math.floor(totalWidth / headers.length));
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((h, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: "D9E2F3" },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true })] })]
    }))
  });
  const dataRows = rows.map(r => new TableRow({
    children: r.map((c, i) => new TableCell({
      width: { size: w[i], type: WidthType.DXA },
      children: [new Paragraph({ text: String(c) })]
    }))
  }));
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: w,
    rows: [headerRow, ...dataRows]
  });
}

function problemBlock(title, problem, cause, investigation, solution, lesson) {
  return [
    H3(title),
    new Paragraph({ children: [new TextRun({ text: "Problem: ", bold: true }), new TextRun({ text: problem })], spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: "Root Cause: ", bold: true }), new TextRun({ text: cause })], spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: "Investigation: ", bold: true }), new TextRun({ text: investigation })], spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: "Solution: ", bold: true }), new TextRun({ text: solution })], spacing: { after: 60 } }),
    new Paragraph({ children: [new TextRun({ text: "Lesson Learned: ", bold: true }), new TextRun({ text: lesson })], spacing: { after: 200 } }),
  ];
}

const children = [];

// ================= TITLE PAGE =================
children.push(
  new Paragraph({ text: "", spacing: { before: 1800 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Data Engineering Interview Prep Guide", bold: true, size: 52 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 300 },
    children: [new TextRun({ text: "Enterprise AI-Augmented E-Commerce Data Platform", size: 30, italics: true })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 200 },
    children: [new TextRun({ text: "Generated Guide", size: 22 })]
  })
);

// ================= TOC =================
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(new Paragraph({ text: "Table of Contents", heading: HeadingLevel.HEADING_1 }));
children.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }));

// ================= CHAPTER 1 =================
children.push(H1("Chapter 1: Project Explanation & Tech Stack"));
children.push(H2("1.1 What is this project, in simple words?"));
children.push(P("This project is an end-to-end data pipeline simulating an e-commerce platform. It generates synthetic customer, product, order, session, and clickstream data, streams it via Kafka, lands it in S3 as a Bronze layer, cleans it with PySpark to a Silver layer, models it into a Star Schema (Gold layer), loads it into Snowflake, and visualizes it in Power BI."));

children.push(H2("1.2 The Tech Stack"));
children.push(simpleTable(
  ["Tool", "Role"],
  [
    ["Python", "Used for data generation, Kafka producer, and Kafka consumer."],
    ["Apache Kafka", "Message broker handling high-throughput streaming of events."],
    ["Amazon S3", "Cloud object storage acting as the Data Lake for Bronze and Silver data."],
    ["PySpark", "Distributed processing engine for ETL/cleaning data."],
    ["Snowflake", "Cloud Data Warehouse storing the Gold layer Star Schema."],
    ["Power BI", "Business intelligence tool connecting to Snowflake for dashboards."]
  ]
));

// ================= CHAPTER 2 =================
children.push(H1("Chapter 2: Dimensional Modeling & Data Warehousing"));
children.push(H2("2.1 Star Schema Design"));
children.push(P("The project uses a Star Schema. Fact Table: fact_orders. Dimension Tables: dim_customer, dim_product, dim_date, dim_session. A Star schema was chosen over a Snowflake schema because it avoids excessive joining, offering better read performance for BI tools like Power BI."));

// ================= CHAPTER 3 =================
children.push(H1("Chapter 3: System Design & Real-Time Streaming"));
children.push(H2("3.1 Fault Tolerance and Scalability"));
children.push(P("Kafka partitions allow parallel consumption (horizontal scaling). Kafka replication ensures fault tolerance. S3 provides 99.999999999% durability. Snowflake elastically scales compute via Virtual Warehouses without moving data."));

// ================= CHAPTER 4 =================
children.push(H1("Chapter 4: Real Production Problems & Debugging"));
children.push(...problemBlock(
  "Issue 1: Small File Problem in S3",
  "Spark job was too slow reading Bronze data.",
  "Consumer was writing one file per message, creating thousands of tiny files.",
  "Checked S3 folder, saw 100,000 files averaging 2KB each.",
  "Modified consumer to batch writes (write every 1,000 messages or 1 minute).",
  "Always batch stream writes into object storage to avoid metadata overhead."
));

// ================= CHAPTER 5 =================
children.push(H1("Chapter 5: Future Optimizations & Resume Pitch"));
children.push(H2("5.1 1-Minute Pitch"));
children.push(P("I built an end-to-end data engineering project simulating an e-commerce platform. A Python script generates synthetic data, pushed to Kafka in real time. A consumer writes raw data to S3 (Bronze). PySpark cleans and validates it into Parquet files (Silver). I modeled a Star Schema and aggregated it into business tables (Gold). Finally, this data is loaded into Snowflake and visualized using Power BI."));

// ================= CHAPTER 6 =================
children.push(H1("Chapter 6: Interview Question Bank"));

children.push(H2("Kafka Questions"));
children.push(...qaBlock("Core Kafka", [
  ["What is a Kafka partition?", "A topic is split into partitions for parallel processing. It is an ordered, immutable sequence of messages."],
  ["What is a consumer group?", "A group of consumers cooperating to read a topic. Each partition is assigned to exactly one consumer in the group."],
  ["What does 'acks=all' mean?", "The producer waits for all in-sync replicas to confirm receipt of the message before considering it successful."]
]));

children.push(H2("PySpark Questions"));
children.push(...qaBlock("Core PySpark", [
  ["What is the difference between transformation and action?", "Transformations are lazy and create a new lineage (e.g., filter, map). Actions trigger the actual execution (e.g., count, collect)."],
  ["What is a shuffle?", "Redistributing data across partitions (and nodes) which is an expensive operation involving disk and network I/O."],
  ["What is the difference between repartition and coalesce?", "Repartition does a full shuffle to increase or decrease partitions. Coalesce only decreases partitions and minimizes shuffling."]
]));

children.push(H2("Snowflake Questions"));
children.push(...qaBlock("Core Snowflake", [
  ["What is a Virtual Warehouse?", "The compute cluster in Snowflake that executes queries, completely separate from storage."],
  ["What is Time Travel?", "Allows accessing historical data (up to 90 days) that was changed or deleted, useful for recovery."],
  ["What is Zero Copy Clone?", "Creates a logical copy of a database/schema/table instantly without consuming additional physical storage until changes are made."]
]));

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullet-list",
        levels: [
          {
            level: 0,
            format: "bullet",
            text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      }
    ]
  },
  sections: [{
    properties: {},
    children: children
  }]
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("Data_Engineering_Interview_Prep_Guide.docx", buffer);
  console.log("Document generated successfully.");
});
