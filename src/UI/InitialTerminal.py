from UI.Terminal import Terminal


class InitialTerminal(Terminal):
    welcome_message = """Welcome to Katharsis!
This is a GUI for the Kathara network simulator.

In order to use this application, you must:
    - Install Docker in rootful mode
    - Add your user to the docker group
    
After making your lab, you will be able to (re)start it from the sidebar.
Wiping will delete all Kathara labs and containers.
You can use the refresh button to detect changes that were made outside of this application.

For a reference on Kathara labs, visit:
https://github.com/KatharaFramework/Kathara-Labs"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run(['echo', self.welcome_message])
