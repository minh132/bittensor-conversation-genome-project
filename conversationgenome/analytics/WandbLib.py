import random
import json
from conversationgenome import __version__ as init_version

verbose = False


from conversationgenome.utils.Utils import Utils
from conversationgenome.ConfigLib import c
from conversationgenome.mock.MockBt import MockBt

bt = None
try:
    import bittensor as bt
except:
    if verbose:
        print("bittensor not installed")
    bt = MockBt()

wandb = None
try:
    import wandb
except:
    print("wandb not installed")


class WandbLib:
    verbose = False

    def init_wandb(self, config=None, data=None):
        wandb_enabled = Utils._int(c.get('env', 'WAND_ENABLED'), 1)
        if not wandb_enabled:
            bt.logging.debug("Weights and Biases Logging Disabled -- Skipping Initialization")
            return
        my_hotkey=12345
        my_uid = -1

        if config:
            #initialize data:
            try:
                wallet = bt.wallet(config=config)
                subtensor = bt.subtensor(config=config)
                metagraph = subtensor.metagraph(config.netuid)
                my_hotkey=wallet.hotkey.ss58_address
                my_uid = metagraph.hotkeys.index(my_hotkey)
            except Exception as e:
                print(f"ERROR 8618322 -- WandB init error: {e}")
                
        
        api = wandb.Api()
        wandb_api_key = c.get("env", "WANDB_API_KEY")
        if not wandb_api_key:
            raise ValueError("Please log in to wandb using `wandb login` or set the WANDB_API_KEY environment variable.")

        bt.logging.info("INIT WANDB", wandb_api_key)

        PROJECT_NAME = 'conversationgenome'
        __version__ = "3.3.0"

        try: 
            __version__ = init_version
        except: 
            print(f"ERROR 1277289 -- WandB version init error: {e}")
        
        run_name = f'cgp/validator-{my_uid}-{__version__}'
        config = {
            "uid": my_uid,
            "hotkey": my_hotkey,
            "version": __version__,
            "type": 'validator',
        }
        wandb.init(
              project=PROJECT_NAME,
              name=run_name, #f"conversationgenome/cguid_{c_guid}",
              entity='afterparty',
              config=config
        )


    def log(self, data):
        wandb_enabled = Utils._int(c.get('env', 'WAND_ENABLED'), 1)
        if wandb_enabled:
            if self.verbose:
                print("WANDB LOG", data)
            wandb.log(data)
        else:
            bt.logging.debug("Weights and Biases Logging Disabled -- Skipping Log")
            return

    def end_log_wandb(self):
        # Mark the run as finished
        wandb.finish()

