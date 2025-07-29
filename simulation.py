from ai_agent import AIAgent
import time

def create_agents():
    # Create the first AI agent
    agent1 = AIAgent(
        name="Sarah Chen",
        age=32,
        occupation="Environmental Scientist",
        personality_traits=["curious", "analytical", "passionate"],
        backstory="I grew up in San Francisco and have always been fascinated by the intersection of technology and environmental conservation. My research focuses on using AI to predict climate patterns."
    )
    agent1.add_interest("environmental science")
    agent1.add_interest("artificial intelligence")
    agent1.add_interest("hiking")
    agent1.add_interest("photography")

    # Create the second AI agent
    agent2 = AIAgent(
        name="Marcus Rodriguez",
        age=28,
        occupation="Digital Artist",
        personality_traits=["creative", "empathetic", "adventurous"],
        backstory="Born in Mexico City but traveled around the world before settling in Toronto. I combine traditional art techniques with AI to create immersive digital experiences."
    )
    agent2.add_interest("digital art")
    agent2.add_interest("cultural exchange")
    agent2.add_interest("technology")
    agent2.add_interest("music")

    return agent1, agent2

def run_simulation():
    agent1, agent2 = create_agents()
    
    print("Starting AI Simulation...")
    print("\nIntroductions:")
    print(f"Agent 1: {agent1.get_introduction()}")
    print(f"Agent 2: {agent2.get_introduction()}")

    # Sample conversation topics
    conversation_starters = [
        "What do you think about the role of AI in creative fields?",
        "How do you spend your free time?",
        "What inspired you to choose your current career?",
        "How do you think technology will change our lives in the next decade?",
    ]

    print("\nStarting conversation...")
    for topic in conversation_starters:
        print(f"\nNew Topic: {topic}")
        # Agent 1 responds to the topic
        response1 = agent1.respond_to(topic, agent2)
        print(f"{agent1.name}: {response1}")
        time.sleep(2)  # Add a small delay to make it more natural

        # Agent 2 responds to Agent 1's response
        response2 = agent2.respond_to(response1, agent1)
        print(f"{agent2.name}: {response2}")
        time.sleep(2)

if __name__ == "__main__":
    run_simulation()
