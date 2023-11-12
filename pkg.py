from cx_Freeze import setup, Executable


setup(
        name='ITCapstone2023Fall',
        version='0.1.0',
        description='IT Capstone project for Fall 2023 with the goal of auction site web development focusing on the use of Chat-GPT. Chris Layson: Project Leader, Njagi Kagika: Researcher/Documenter/AI Evanluation, Ismail Lawal: Researcher/Documenter/Initially UI(UX), Christian Bush: Front-End/Researcher, Zach Nash: Back-End/Researcher',
        executables=[Executable('run.py', base=None)],
        
        options={'build_exe':{
            'include_files': ['app'],
            'excludes': ['.vs', '_pycache_', 'venv', 'auction_website.db', 'error_log.log', 'secret_key.txt']
        }
    }
)