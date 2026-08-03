import React from 'react';
import Navbar from '../components/Navbar';
import ArticleHeader from '../components/ArticleHeader';
import ArchitectureImage from '../components/ArchitectureImage';
import Section from '../components/Section';
import TechTable from '../components/TechTable';
import CodeBlock from '../components/CodeBlock';
import Footer from '../components/Footer';
import AboutAuthor from '../components/AboutAuthor';

// Use placeholder paths for development, will be replaced with actual image assets later
import architectureImg from '../assets/architecture.png';
import agentArchitectureImg from '../assets/agent-architecture.png';

const Home = () => {
  const mcpToolsData = [
    { Tool: 'glue_job_status()', Purpose: 'Check Glue JobRun status' },
    { Tool: 'bronze_to_silver_status()', Purpose: 'Monitor Bronze → Silver ETL' },
    { Tool: 'silver_to_gold_status()', Purpose: 'Monitor Silver → Gold ETL' },
    { Tool: 'get_table_schema()', Purpose: 'Retrieve Glue Catalog metadata' },
    { Tool: 'run_athena_query()', Purpose: 'Execute read-only Athena SELECT queries' }
  ];

  const techStackData = [
    { Category: 'Programming', Technology: 'Python, SQL' },
    { Category: 'Streaming', Technology: 'Apache Kafka' },
    { Category: 'Cloud', Technology: 'AWS' },
    { Category: 'Data Lake', Technology: 'Amazon S3' },
    { Category: 'ETL', Technology: 'AWS Glue' },
    { Category: 'Processing', Technology: 'Apache Spark, PySpark' },
    { Category: 'Format', Technology: 'Apache Parquet' },
    { Category: 'Metadata', Technology: 'AWS Glue Data Catalog' },
    { Category: 'Analytics', Technology: 'Amazon Athena' },
    { Category: 'Orchestration', Technology: 'Apache Airflow' },
    { Category: 'Containerization', Technology: 'Docker' },
    { Category: 'DataOps', Technology: 'GitHub Actions' },
    { Category: 'AI', Technology: 'Amazon Bedrock, Claude' },
    { Category: 'AI Integration', Technology: 'Model Context Protocol' },
    { Category: 'AWS SDK', Technology: 'Boto3' },
    { Category: 'Security', Technology: 'AWS IAM' },
    { Category: 'Modeling', Technology: 'Star Schema' }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-white">
      <Navbar />
      
      <main className="flex-grow w-full px-4 sm:px-6 lg:px-8 py-10 max-w-article mx-auto">
        <ArticleHeader />
        
        <AboutAuthor />
        
        <article className="prose prose-lg max-w-none prose-blue">
          
          <Section title="Overview">
            <p>
              This project demonstrates the design and implementation of an enterprise-grade 
              e-commerce data engineering platform on AWS.
            </p>
            <p>
              The platform combines:
            </p>
            <ul className="list-disc pl-6 space-y-2 mt-4 mb-8">
              <li>Real-time event streaming</li>
              <li>Medallion Architecture</li>
              <li>Distributed PySpark processing</li>
              <li>Metadata management</li>
              <li>Serverless SQL analytics</li>
              <li>Workflow orchestration</li>
              <li>DataOps / CI</li>
              <li>Agentic AI using Bedrock + MCP</li>
            </ul>
          </Section>

          <Section title="Solution Architecture">
            <p>
              The architecture is designed to handle large-scale, real-time data ingestion 
              while providing a robust foundation for analytics and AI agent integration. 
              Data flows systematically through Bronze, Silver, and Gold layers.
            </p>
            <ArchitectureImage 
              src={architectureImg}
              alt="Architecture Diagram" 
              caption="Figure 1 — End-to-End Architecture of the AI-Augmented E-Commerce Data Engineering Platform on AWS"
            />
          </Section>

          <Section title="Architecture Flow">
            <div className="bg-gray-50 border border-gray-200 p-8 rounded text-center font-mono text-sm leading-relaxed mb-8 shadow-inner">
              <div className="flex flex-col items-center justify-center space-y-3">
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">Python Data Generator</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">Apache Kafka</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">Python Kafka Consumer</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-blue-700 bg-blue-50 px-4 py-2 border border-blue-200 rounded shadow-sm">Amazon S3 Bronze</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">AWS Glue Crawler</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">AWS Glue Data Catalog</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">AWS Glue + PySpark</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-600 bg-gray-100 px-4 py-2 border border-gray-300 rounded shadow-sm">Amazon S3 Silver</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">AWS Glue + PySpark</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-yellow-600 bg-yellow-50 px-4 py-2 border border-yellow-200 rounded shadow-sm">Amazon S3 Gold</span>
                <span className="text-gray-400">↓</span>
                <span className="font-bold text-gray-800 bg-white px-4 py-2 border rounded shadow-sm">Amazon Athena</span>
              </div>
            </div>
          </Section>

          <Section title="Medallion Architecture">
            <div className="space-y-10">
              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 border-l-4 border-amber-700 pl-4">01 — Bronze Layer</h3>
                <p className="mb-2"><strong>Storage:</strong> Amazon S3</p>
                <p>
                  Raw e-commerce events received from Kafka are stored without business transformations. 
                  Data is kept in its original <strong>JSON</strong> format as an immutable source of truth.
                </p>
              </div>

              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 border-l-4 border-gray-400 pl-4">02 — Silver Layer</h3>
                <p className="mb-2"><strong>Processing & Storage:</strong> Amazon S3 + AWS Glue + PySpark</p>
                <p>
                  Raw data is cleaned, standardized, validated and converted into highly optimized <strong>Apache Parquet</strong> format.
                </p>
                <p className="mt-3 font-semibold">Operations:</p>
                <ul className="list-disc pl-6 space-y-1 mt-2">
                  <li>Schema validation</li>
                  <li>Null handling</li>
                  <li>Deduplication</li>
                  <li>Type casting</li>
                  <li>Data standardization</li>
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-bold text-gray-900 mb-3 border-l-4 border-yellow-500 pl-4">03 — Gold Layer</h3>
                <p className="mb-2"><strong>Storage:</strong> Amazon S3</p>
                <p>
                  Business-ready analytical datasets are created using dimensional modeling. 
                  The data is organized into a robust Star Schema optimized for BI tools and Athena querying.
                </p>
                
                <div className="mt-6 bg-gray-50 border border-gray-200 p-6 rounded text-center">
                  <p className="font-bold mb-4 text-sm uppercase text-gray-500 tracking-widest">Star Schema</p>
                  <div className="font-mono text-gray-800 font-semibold text-lg flex items-center justify-center space-x-4">
                    <span>dim_date</span>
                    <span className="text-gray-400">—</span>
                    <div className="flex flex-col items-center">
                      <span className="mb-2 text-gray-400">dim_customer</span>
                      <span className="text-gray-400">|</span>
                      <span className="bg-white border-2 border-yellow-400 px-4 py-2 rounded shadow-sm z-10">fact_orders</span>
                    </div>
                    <span className="text-gray-400">—</span>
                    <span>dim_product</span>
                  </div>
                </div>
              </div>
            </div>
          </Section>

          <Section title="Real-Time Data Ingestion with Apache Kafka">
            <p>
              The streaming pipeline begins with a Python synthetic data generator simulating realistic 
              e-commerce traffic. This data flows through a Kafka Producer into dedicated topics, 
              which are then continuously polled by a Consumer and dumped into the Bronze bucket.
            </p>
            
            <CodeBlock 
              language="python" 
              code={`# Kafka Producer Example
from confluent_kafka import Producer
import json

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Simulating an e-commerce event
event = {
    "order_id": "ORD-123",
    "customer_id": "CUST-456",
    "amount": 199.99
}

producer.produce(
    'ecommerce_events', 
    json.dumps(event).encode('utf-8'), 
    callback=delivery_report
)
producer.flush()`} 
            />
          </Section>

          <Section title="Data Transformation with AWS Glue and PySpark">
            <p>
              AWS Glue serves as the backbone for distributed ETL processing. We leverage Glue Crawlers 
              to automatically discover schemas and maintain the Data Catalog.
            </p>
            
            <div className="my-8 space-y-6">
              <div className="flex items-center space-x-4 text-sm font-mono bg-gray-50 p-4 rounded border">
                <span className="font-bold">Bronze</span>
                <span className="text-gray-400">→</span>
                <span>Glue Crawler</span>
                <span className="text-gray-400">→</span>
                <span>Glue Data Catalog</span>
                <span className="text-gray-400">→</span>
                <span>Glue PySpark ETL</span>
                <span className="text-gray-400">→</span>
                <span className="font-bold">Silver</span>
              </div>
              
              <div className="flex items-center space-x-4 text-sm font-mono bg-gray-50 p-4 rounded border">
                <span className="font-bold">Silver</span>
                <span className="text-gray-400">→</span>
                <span>Glue Crawler</span>
                <span className="text-gray-400">→</span>
                <span>Glue PySpark ETL</span>
                <span className="text-gray-400">→</span>
                <span className="font-bold">Gold</span>
              </div>
            </div>
          </Section>

          <Section title="Serverless Analytics with Amazon Athena">
            <p>
              Amazon Athena provides a serverless SQL interface to directly query the Gold datasets stored in Amazon S3, 
              using the metadata maintained by the AWS Glue Data Catalog. 
              <strong> Athena does NOT store the Gold data itself</strong>; it computes the queries in memory and returns the results.
            </p>

            <CodeBlock 
              language="sql"
              code={`-- Example Athena Query querying the S3 Gold Layer
SELECT 
    dp.category,
    SUM(fo.amount) as total_revenue
FROM ai_augmented_gold_db.fact_orders fo
JOIN ai_augmented_gold_db.dim_product dp 
  ON fo.product_key = dp.product_key
GROUP BY dp.category
ORDER BY total_revenue DESC;`}
            />
          </Section>

          <Section title="Pipeline Orchestration with Apache Airflow">
            <p>
              To manage complex dependencies between crawlers and ETL scripts, we use Apache Airflow running in Docker. 
              Airflow orchestrates the execution of the AWS jobs but <strong>does not</strong> perform the heavy lifting of PySpark transformations itself.
            </p>
            
            <div className="flex flex-wrap items-center justify-center gap-3 text-sm font-mono bg-gray-50 p-6 rounded border my-8">
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Docker</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded font-bold text-red-600">Apache Airflow</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Bronze Crawler</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Bronze-to-Silver ETL</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Silver Crawler</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Silver-to-Gold ETL</span>
              <span className="text-gray-400">→</span>
              <span className="bg-white px-3 py-1 border shadow-sm rounded">Gold Crawler</span>
            </div>
          </Section>

          <Section title="DataOps with GitHub Actions">
            <p>
              Robust DataOps principles are implemented via GitHub Actions to ensure code quality and deployment safety.
            </p>
            
            <div className="flex items-center space-x-4 text-sm font-mono bg-gray-50 p-4 rounded border mb-6">
              <span className="font-bold">Developer</span>
              <span className="text-gray-400">→</span>
              <span>Git</span>
              <span className="text-gray-400">→</span>
              <span>GitHub</span>
              <span className="text-gray-400">→</span>
              <span className="font-bold text-gray-800">GitHub Actions</span>
            </div>
            
            <p className="font-semibold mb-2">GitHub Actions performs:</p>
            <ul className="list-disc pl-6 space-y-1">
              <li>Python validation (linting/formatting)</li>
              <li>Code-quality checks</li>
              <li>Airflow DAG validation</li>
              <li>Security checks</li>
              <li>Secret scanning</li>
            </ul>
          </Section>

          <Section title="AI Data Engineering Agent">
            <p>
              The most advanced feature of this platform is the AI Data Engineering Agent. By integrating Amazon Bedrock 
              and Anthropic's Claude Haiku 4.5 via the Model Context Protocol (MCP), we give natural language 
              access to live data engineering operations.
            </p>
            
            <ArchitectureImage 
              src={agentArchitectureImg}
              alt="AI Agent Architecture Diagram" 
              caption="Figure 2 — AI Agent Architecture leveraging Model Context Protocol (MCP) and Amazon Bedrock"
            />
          </Section>

          <Section title="Model Context Protocol Integration">
            <p>
              The MCP server exposes critical read-only AWS operations to Claude, allowing the LLM to autonomously 
              gather context and execute queries without compromising security.
            </p>
            
            <TechTable 
              columns={['Tool', 'Purpose']} 
              data={mcpToolsData} 
            />
          </Section>
          
          <Section title="How the AI Agent Works">
            <p className="mb-6">
              When a user asks a complex business question, Claude uses its reasoning capabilities to sequentially 
              query schemas, construct SQL, execute it via Athena, and return a final natural language answer.
            </p>
            
            <div className="bg-white border-2 border-gray-100 rounded p-8 shadow-sm max-w-2xl mx-auto my-8 font-mono text-sm">
              <div className="flex flex-col space-y-4">
                <div className="bg-blue-50 border border-blue-200 text-blue-900 p-4 rounded-lg">
                  <span className="font-bold">User:</span> "Which product category generated the highest revenue?"
                </div>
                
                <div className="text-center text-gray-400">↓</div>
                
                <div className="bg-gray-50 border border-gray-200 text-center p-3 rounded font-bold text-gray-700">
                  Claude Haiku 4.5
                </div>
                
                <div className="text-center text-gray-400">↓</div>
                
                <div className="bg-gray-800 text-white border border-gray-700 text-center p-2 rounded">
                  MCP Tool Selection
                </div>
                
                <div className="text-center text-gray-400">↓</div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white border border-gray-300 text-center p-3 rounded shadow-sm text-xs">
                    <code className="text-purple-600 font-bold">get_table_schema()</code><br/>
                    <span className="text-gray-500 mt-1 block">Fetch tables</span>
                  </div>
                  <div className="bg-white border border-gray-300 text-center p-3 rounded shadow-sm text-xs">
                    <code className="text-green-600 font-bold">run_athena_query()</code><br/>
                    <span className="text-gray-500 mt-1 block">Execute SQL</span>
                  </div>
                </div>
                
                <div className="text-center text-gray-400">↓</div>
                
                <div className="bg-yellow-50 border border-yellow-300 text-center p-3 rounded font-bold text-yellow-800">
                  Gold Star Schema (Amazon Athena)
                </div>
                
                <div className="text-center text-gray-400">↓</div>
                
                <div className="bg-green-50 border border-green-200 text-green-900 p-4 rounded-lg">
                  <span className="font-bold">Agent Answer:</span> "The product category that generated the highest revenue is Books with $299,034."
                </div>
              </div>
            </div>
          </Section>

          <Section title="Technology Stack">
            <TechTable 
              columns={['Category', 'Technology']} 
              data={techStackData} 
            />
          </Section>

        </article>
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;
