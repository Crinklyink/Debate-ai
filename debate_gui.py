import tkinter as tk
from tkinter import ttk, scrolledtext
from ai_agent import AIAgent
from settings_manager import SettingsManager
import threading
import time

class DebateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Debate Simulator")
        
        # Create main windows
        self.create_chat_window()
        self.create_summary_window()
        
        # Initialize agents
        self.agent1 = None
        self.agent2 = None
        
        # Settings manager
        self.settings_manager = None
        
        # Add settings button to the main window
        self.settings_button = ttk.Button(
            self.root,
            text="⚙️ Settings",
            command=self.open_settings
        )
        self.settings_button.pack(pady=5)
        
        # Debate control
        self.create_debate_controls()
        
        self.summary = []
        self.is_debating = False
        self.current_responses = {}
        self.debate_thread = None  # Track the debate thread
        self.gui_alive = True  # Track if GUI is still active
        
        # Bind window close events
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.summary_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_chat_window(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Debate Chat")
        self.chat_window.geometry("800x800")
        
        self.chat_area = scrolledtext.ScrolledText(self.chat_window, wrap=tk.WORD, height=40, font=("Consolas", 10))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def create_summary_window(self):
        self.summary_window = tk.Toplevel(self.root)
        self.summary_window.title("Debate Summary")
        self.summary_window.geometry("400x800")
        
        self.summary_area = scrolledtext.ScrolledText(self.summary_window, wrap=tk.WORD, height=40, font=("Consolas", 10))
        self.summary_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def create_debate_controls(self):
        # Top control frame for topic and buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Web research toggle
        self.web_research = tk.BooleanVar(value=False)
        research_frame = ttk.LabelFrame(control_frame, text="Research Mode")
        research_frame.pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(research_frame, text="Enable Web Research", variable=self.web_research).pack(side=tk.LEFT)
        
        # Topic entry
        ttk.Label(control_frame, text="Debate Topic:").pack(side=tk.LEFT)
        self.topic_entry = ttk.Entry(control_frame, width=50)
        self.topic_entry.pack(side=tk.LEFT, padx=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Debate", command=self.start_debate)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", command=self.stop_debate)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.config(state=tk.DISABLED)
        
        self.clear_button = ttk.Button(control_frame, text="Clear Debate", command=self.clear_debate)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Score frame for tracking points
        score_frame = ttk.Frame(self.root)
        score_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Agent 1 score controls
        agent1_frame = ttk.LabelFrame(score_frame, text="Jamal Carter")
        agent1_frame.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.agent1_score = tk.IntVar(value=0)
        ttk.Label(agent1_frame, text="Score:").pack(side=tk.LEFT)
        ttk.Label(agent1_frame, textvariable=self.agent1_score).pack(side=tk.LEFT)
        ttk.Button(agent1_frame, text="+1", command=lambda: self.update_score(1, 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(agent1_frame, text="-1", command=lambda: self.update_score(1, -1)).pack(side=tk.LEFT, padx=2)
        
        # Agent 2 score controls
        agent2_frame = ttk.LabelFrame(score_frame, text="Andrew Wallace")
        agent2_frame.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.agent2_score = tk.IntVar(value=0)
        ttk.Label(agent2_frame, text="Score:").pack(side=tk.LEFT)
        ttk.Label(agent2_frame, textvariable=self.agent2_score).pack(side=tk.LEFT)
        ttk.Button(agent2_frame, text="+1", command=lambda: self.update_score(2, 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(agent2_frame, text="-1", command=lambda: self.update_score(2, -1)).pack(side=tk.LEFT, padx=2)
        
        # Adjust main window size to fit new controls
        self.root.geometry("600x150")

    def add_to_chat(self, message, agent_name):
        self.chat_area.insert(tk.END, f"{agent_name}: {message}\n\n")
        # Get current view
        first_visible = self.chat_area.yview()[0]
        last_visible = self.chat_area.yview()[1]
        
        # Only auto-scroll if we're already at the bottom
        if last_visible == 1.0:
            self.chat_area.see(tk.END)
            self.chat_area.update()

    def update_score(self, agent_num, delta):
        """Update the score for an agent"""
        if agent_num == 1:
            self.agent1_score.set(self.agent1_score.get() + delta)
            name = "Jamal Carter"
        else:
            self.agent2_score.set(self.agent2_score.get() + delta)
            name = "Andrew Wallace"
            
        score = self.agent1_score.get() if agent_num == 1 else self.agent2_score.get()
        self.add_to_summary(f"Point {'awarded to' if delta > 0 else 'deducted from'} {name} (Score: {score})")
        
    def clear_debate(self):
        """Clear all debate text and summaries"""
        self.chat_area.delete(1.0, tk.END)
        self.summary_area.delete(1.0, tk.END)
        self.summary = []
        self.current_responses = {}
        self.agent1_score.set(0)
        self.agent2_score.set(0)
        self.add_to_chat("Debate cleared. Enter a new topic to begin.", "System")
        
    def safe_update_gui(self, func):
        """Safely execute GUI updates in the main thread"""
        if not self.gui_alive:
            return
        try:
            if threading.current_thread() is threading.main_thread():
                func()
            else:
                self.root.after(0, func)
        except tk.TclError:
            self.gui_alive = False

    def stream_response(self, name, response, streaming=False):
        """Handle streaming responses with proper text updating"""
        if not self.gui_alive:
            return

        def update_text():
            try:
                # Initialize response tracking if needed
                if name not in self.current_responses:
                    self.current_responses[name] = ""
                    self.chat_area.insert(tk.END, f"\n{name}: ")
                
                if streaming and response:
                    # Append the new text
                    self.chat_area.insert(tk.END, response)
                    self.current_responses[name] += response
                elif not streaming:
                    # End of response - add newlines if we got any content
                    if self.current_responses[name]:
                        self.chat_area.insert(tk.END, "\n\n")
                
                # Force update and scroll if at bottom
                self.chat_area.update()
                if self.chat_area.yview()[1] == 1.0:
                    self.chat_area.see(tk.END)
            except tk.TclError:
                self.gui_alive = False
            

        self.safe_update_gui(update_text)

    def add_to_summary(self, summary):
        self.summary.append(summary)
        self.summary_area.delete(1.0, tk.END)
        for s in self.summary[-10:]:  # Keep last 10 summaries
            self.summary_area.insert(tk.END, f"• {s}\n\n")
        self.summary_area.see(tk.END)

    def start_debate(self):
        if not self.agent1 or not self.agent2:
            self.add_to_chat("Please set up the agents first!", "System")
            return

        topic = self.topic_entry.get().strip()
        if not topic:
            self.add_to_chat("Please enter a debate topic!", "System")
            return

        self.is_debating = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Clear any existing responses
        self.current_responses.clear()
        
        # Start debate in a separate thread
        self.debate_thread = threading.Thread(target=self.run_debate, args=(topic,))
        self.debate_thread.daemon = True
        self.debate_thread.start()

    def on_close(self):
        """Handle window closing"""
        self.gui_alive = False
        self.is_debating = False
        if self.debate_thread and self.debate_thread.is_alive():
            self.debate_thread.join(timeout=1)
        try:
            self.chat_window.destroy()
            self.summary_window.destroy()
            self.root.destroy()
        except:
            pass

    def stop_debate(self):
        """Stop the current debate"""
        self.is_debating = False
        if self.gui_alive:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        self.current_responses.clear()  # Clear current responses tracking
        if self.debate_thread and self.debate_thread.is_alive():
            self.debate_thread.join(timeout=1)  # Wait for thread to finish
        if self.gui_alive:
            self.add_to_chat("\n=== Debate paused. Click Start to continue ===\n", "System")

    def open_settings(self):
        """Open the settings manager window"""
        if not self.agent1 or not self.agent2:
            # Create agents first if they don't exist
            self.create_agents()
        
        if not self.settings_manager:
            self.settings_manager = SettingsManager(self.root, [self.agent1, self.agent2])

    def run_debate(self, topic):
        self.current_responses.clear()  # Clear any previous response tracking
        self.add_to_chat(f"=== Debate Topic: {topic} ===\n", "System")
        self.add_to_summary(f"New debate started on: {topic}")
        
        # Determine interaction mode
        mode_type = "collaborative discussion" if (self.settings_manager and 
            self.settings_manager.mode_var.get() == "collaborate") else "debate"
            
        # Build appropriate context based on mode
        format_points = {
            'collaborative discussion': [
                "Draw from their unique expertise and perspective",
                "Support arguments with relevant examples and build on each other's points",
                "Maintain professional discourse while staying true to their personality",
                "Work together to find comprehensive answers",
                "Keep responses focused and concise (2-3 paragraphs)"
            ],
            'debate': [
                "Draw from their unique expertise and perspective",
                "Support arguments with relevant examples",
                "Maintain professional discourse while staying true to their personality",
                "Consider and respond to the other's viewpoints thoughtfully",
                "Keep responses focused and concise (2-3 paragraphs)"
            ]
        }
        
        points = format_points[mode_type]
        debate_context = f"""This is an intellectual {mode_type} on the topic: {topic}
        
Format: This is a {'collaborative' if mode_type == 'collaborative discussion' else 'respectful academic'} discussion between two experts. Each participant should:
- {points[0]}
- {points[1]}
- {points[2]}
- {points[3]}
- {points[4]}"""
        
        self.add_to_chat("\nOpening Statements:\n", "System")
        self.current_responses.clear()
        
        # Initial statements
        if self.is_debating:
            # Use settings manager's web research setting if available
            web_research_enabled = (self.settings_manager.get_web_research_enabled() 
                                  if self.settings_manager else self.web_research.get())
            
            response1 = self.agent1.respond_to(
                f"Make your opening statement on why your position on {topic} is correct. Be focused and persuasive.",
                self.agent2,
                debate_context,
                callback=self.stream_response,
                web_research=web_research_enabled
            )
            if not self.is_debating:
                return
            
            time.sleep(2)
            
            if self.is_debating and not self.current_responses.get(self.agent2.name):
                web_research_enabled = (self.settings_manager.get_web_research_enabled() 
                                      if self.settings_manager else self.web_research.get())
                
                response2 = self.agent2.respond_to(
                    response1,
                    self.agent1,
                    debate_context,
                    callback=self.stream_response,
                    web_research=web_research_enabled
                )
                if not self.is_debating:
                    return
        
        # Continue debate indefinitely until stopped
        last_response = response2 if 'response2' in locals() else ""
        current_agent = self.agent1
        other_agent = self.agent2
        
        rounds = 0
        while self.is_debating:  # No round limit
            time.sleep(2)  # Add delay between responses
            
            if not self.is_debating:
                break
                
            # Update debate context with round information
            round_context = f"{debate_context}\n\nThis is round {rounds + 1} of the discussion. Consider previous points raised and develop the conversation further."
            
            # Clear the current agent's response tracking before their new response
            if current_agent.name in self.current_responses:
                del self.current_responses[current_agent.name]
            
            web_research_enabled = (self.settings_manager.get_web_research_enabled() 
                                  if self.settings_manager else self.web_research.get())
                                  
            response = current_agent.respond_to(
                last_response,
                other_agent,
                round_context,
                callback=self.stream_response,
                web_research=web_research_enabled
            )
            
            if not self.is_debating:
                break
                
            # Create a more detailed summary
            key_points = response[:100] + "..."  # First 100 characters for summary
            self.add_to_summary(f"Round {rounds + 1}: {current_agent.name} - {key_points}")
            
            # Swap agents
            current_agent, other_agent = other_agent, current_agent
            last_response = response
            rounds += 1

def setup_agents():
    jamal = AIAgent(
        name="Jamal Carter",
        age=30,
        occupation="Cognitive Neuroscientist",
        personality_traits=[
            "analytical",
            "emotionally intelligent",
            "charismatic",
            "warm",
            "confident"
        ],
        backstory="""A rising star in cognitive neuroscience, specializing in memory formation and emotional perception, 
        particularly in relation to artificial intelligence. Double majored in neuroscience and philosophy at Columbia, 
        followed by a PhD at MIT. Currently works in the Harvard/MIT research district in Boston. Deeply passionate about 
        the boundary between human consciousness and machine learning. Publications in major journals, regular TED Talk speaker, 
        and podcast guest. Volunteers for mental health outreach, mentors underrepresented students, and plays jazz piano.""",
        model="dolphin-mixtral:latest"
    )
    
    andrew = AIAgent(
        name="Andrew Wallace",
        age=33,
        occupation="Theoretical Physicist & Computational Engineer",
        personality_traits=[
            "reserved",
            "logical",
            "witty",
            "intensely curious",
            "precise"
        ],
        backstory="""A theoretical physicist working at the intersection of quantum computing and AI in Seattle. 
        PhD from Caltech in quantum field theory before pivoting to applied research in large-scale computation 
        and entropy modeling for AGI systems. Works at a private research institute building frameworks for machine 
        learning models that reflect physical systems. Treats intelligence like an emergent force in a structured universe. 
        Known for scientific coffee brewing, retro computer restoration, and writing witty technical blog posts.""",
        model="dolphin-mixtral:latest"
    )
    
    # Add interests to each agent
    jamal.add_interest("neuroscience")
    jamal.add_interest("artificial intelligence")
    jamal.add_interest("consciousness")
    jamal.add_interest("emotional intelligence")
    jamal.add_interest("jazz music")
    jamal.add_interest("mental health")
    
    andrew.add_interest("quantum computing")
    andrew.add_interest("theoretical physics")
    andrew.add_interest("AGI systems")
    andrew.add_interest("computational frameworks")
    andrew.add_interest("retro computing")
    andrew.add_interest("coffee brewing")
    
    return jamal, andrew

def main():
    root = tk.Tk()
    root.title("AI Debate Control")
    root.geometry("600x100")
    
    app = DebateGUI(root)
    
    # Set up agents
    app.agent1, app.agent2 = setup_agents()
    
    root.mainloop()

if __name__ == "__main__":
    main()
