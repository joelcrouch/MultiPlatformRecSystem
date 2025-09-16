import asyncio
import json
import aioredis
from kafka import KafkaConsumer, KafkaProducer

class RealtimeRecommendationPipeline:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'user_interactions',
            bootstrap_servers=['localhost:9092'],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest' # Start from the beginning of the topic
        )
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.redis = None

    async def connect_redis(self):
        """Connects to Redis."""
        self.redis = await aioredis.from_url("redis://localhost")

    async def update_user_profile(self, interaction):
        """
        Updates the user's profile in Redis based on the interaction.
        This is a placeholder for now.
        """
        user_id = interaction.get('user_id')
        if user_id:
            print(f"Updating profile for user: {user_id}")
            # Example: Store the last interacted item
            await self.redis.hset(f"user:{user_id}", "last_interaction", json.dumps(interaction))

    def should_trigger_update(self, interaction):
        """
        Determines if an incremental model update should be triggered.
        This is a placeholder for now.
        """
        # Example: Trigger an update for every 'purchase' interaction
        return interaction.get('interaction_type') == 'purchase'

    async def trigger_model_update(self, interaction):
        """
        Triggers an incremental model update.
        This is a placeholder for now.
        """
        print(f"Triggering model update for interaction: {interaction}")
        # In a real system, this would send a message to a model training service
        self.producer.send('model_update_topic', {'interaction': interaction})


    async def process_interaction_stream(self):
        """Process real-time interactions and update recommendations"""
        await self.connect_redis()
        print("Real-time pipeline started. Waiting for user interactions...")
        for message in self.consumer:
            interaction = message.value
            print(f"Received interaction: {interaction}")

            # Update user profile in real-time
            await self.update_user_profile(interaction)

            # Trigger incremental model update if needed
            if self.should_trigger_update(interaction):
                await self.trigger_model_update(interaction)

if __name__ == '__main__':
    pipeline = RealtimeRecommendationPipeline()
    asyncio.run(pipeline.process_interaction_stream())
