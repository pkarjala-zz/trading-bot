"""Telegram bot for user communication."""
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ..config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self, portfolio_manager=None):
        self.portfolio_manager = portfolio_manager
        self.app = None
    
    async def start(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            'Trading Bot active.\n'
            '/portfolio - Show portfolio\n'
            '/prices - Current prices\n'
            '/alerts - Manage alerts\n'
            '/recommend - Get recommendations\n'
            '/backtest - Run backtest'
        )
    
    async def portfolio(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if self.portfolio_manager:
            pos = self.portfolio_manager.get_positions()
            cash = self.portfolio_manager.get_cash()
            await update.message.reply_text(f'Cash: ${cash:.2f}\nPositions: {pos}')
        else:
            await update.message.reply_text('Portfolio manager not initialized.')
    
    async def prices(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Use /fetch to update prices first.')
    
    async def recommend(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Recommendation engine coming soon.')
    
    async def backtest_cmd(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Run backtest: `python -m src.backtest <symbol>`', parse_mode='Markdown')
    
    def run(self):
        if not TELEGRAM_BOT_TOKEN:
            logger.warning('TELEGRAM_BOT_TOKEN not set, skipping Telegram bot.')
            return
        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler('start', self.start))
        self.app.add_handler(CommandHandler('portfolio', self.portfolio))
        self.app.add_handler(CommandHandler('prices', self.prices))
        self.app.add_handler(CommandHandler('recommend', self.recommend))
        self.app.add_handler(CommandHandler('backtest', self.backtest_cmd))
        logger.info('Telegram bot starting.')
        self.app.run_polling()
