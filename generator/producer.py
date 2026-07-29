import json
import time
from pathlib import Path
import pandas as pd
from kafka import KafkaProducer
from generator.config import KAFKA_BOOTSTRAP_SERVERS, DATA_FILES, TOPICS

class EnterpriseProducer:
    """
    Enterprise-grade Kafka Producer that streams events from multiple datasets simultaneously.
    """

    def __init__(self):
        # Initialize Kafka Producer with JSON serializer
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        except Exception as e:
            print(f"Failed to initialize Kafka Producer: {e}")
            self.producer = None
            
        self.datasets = {}
        self.lengths = {}

    def load_data(self):
        """
        Load all CSV datasets into memory. Missing datasets will be skipped gracefully.
        """
        print("=" * 60)
        print("= Enterprise Producer Started =")
        print("=" * 60)
        
        # Get the project root directory based on the location of this file
        project_root = Path(__file__).resolve().parent.parent
        
        for name, rel_path in DATA_FILES.items():
            file_path = project_root / rel_path
            
            try:
                # Attempt to read the dataset if it exists
                if file_path.exists():
                    df = pd.read_csv(file_path)
                    
                    # Convert dataframe to a list of dictionaries for easy streaming
                    self.datasets[name] = df.to_dict(orient="records")
                    self.lengths[name] = len(self.datasets[name])
                    
                    print(f"Loaded {name} : {self.lengths[name]} rows")
                else:
                    print(f"Warning: Dataset for {name} missing at {file_path}. Skipping.")
            except Exception as e:
                print(f"Error loading {name} from {file_path}: {e}")

    def stream_data(self):
        """
        Publish one event from each available dataset in every iteration (round-robin).
        """
        if not self.producer:
            print("Producer not initialized properly. Cannot stream.")
            return

        print("\n" + "=" * 60)
        print("Streaming Events")
        print("=" * 60)
        
        if not self.datasets:
            print("No datasets loaded. Exiting.")
            return

        # Find the maximum number of rows among loaded datasets
        max_rows = max(self.lengths.values())

        # Iterate through the datasets round-robin
        for i in range(max_rows):
            for name, records in self.datasets.items():
                if i < self.lengths[name]:
                    topic = TOPICS[name]
                    event = records[i]
                    
                    try:
                        self.producer.send(topic, value=event)
                        print(f"[{topic}]")
                    except Exception as e:
                        print(f"Failed to send event for {name} to {topic}: {e}")
                        
            # Flush after every round of sending to ensure delivery
            self.producer.flush()
            
            # Simulate a small delay between event groups
            time.sleep(0.5)

if __name__ == "__main__":
    producer = EnterpriseProducer()
    producer.load_data()
    producer.stream_data()