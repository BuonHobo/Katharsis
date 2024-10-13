from UI.Terminal import Terminal


class InitialTerminal(Terminal):
    welcome_message = """Welcome to Katharsis!
This is a GUI for the Kathara network emulator.

In order to use this application, you must:
    - Install Docker in rootful mode
    - Add your user to the docker group
    
After making your lab, you will be able to (re)start it from the sidebar.
Wiping will delete all Kathara labs and containers.
You can use the refresh button to detect changes that were made outside of this application.

For a Kathara lab reference, visit:
https://github.com/KatharaFramework/Kathara-Labs

If you want to use the integrated terminal for a traditional Kathara experience,
then you must manually give this app permission to access your lab directories.
Flatseal is a great way to do it."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run(['echo', self.welcome_message])
