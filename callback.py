import logging
from datetime import time

from telegram.ext import (
    Updater, 
    CallbackContext,
)

from api import BinanceAPI
from solver import Solver


class CallBacks:
    @staticmethod
    def dashboard_callback(updater: Updater, context: CallbackContext) -> None:
        """
        - Plot fear and greed + open interest + altcoin season index
        - show value fear and greed, open interest, altcoin season index
        - show
        """
        pass

    @staticmethod
    def cdc_callback(update: Updater, context: CallbackContext) -> None:
        args = context.args

        if len(args) > 1:
            context.bot.send_message(
                chat_id=update.effective_chat.id, 
                text="Please parse only one argument!"
            )
        else:
            coin: str = args[0].upper().strip()

            symbol = coin+"USDT"
            interval = "1d"

            logging.info(f"computing {symbol} pair...")

            try:
                candle_data = BinanceAPI.generate_candle_data(symbol, interval)
                _, template = Solver.solve_cdc_cross(candle_data)
                context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=template
                )
            except AssertionError as e:
                logging.info(f"cannot compute with the following error message:\n{e}")
                context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=f"Unrecognize pair name `{symbol}` on Binance"
                )