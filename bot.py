# file: cbse_bot.py
# Requires: python-telegram-bot==20.*
# Install: pip install python-telegram-bot==20.6

import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------------------
# FULLY UPDATED PAPERS DATABASE (CLASS 10)
# -----------------------------------------

PAPERS = {
    "9": {},  # अभी खाली - बाद में तुम लिंक दोगे तो मैं डाल दूँगा

    "10": {
        "English": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1BFXQdLjhHa5KQfWF9TvpaCsvKUsGtORK"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1I3tOya2VSbWt4Ldw3y45gRKDx6Rpbf-F"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=1UrDQRIvm_DdmavtyrHrdQzIkSrOTIDkU"
            ]
        },

        "Hindi": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1nEj7hzSKCmDbpiPFBBsMh760cdyvMGGu"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1cR5wzJmyxr1Z2EjrhSVykNe6WsB83QnQ"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=1Hu-YGSyKwfd3rgPC1TpmWQZrrPnENXTN"
            ]
        },

        "Maths Basic": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1FU663n_w307ndeMOSl9JoinD_517tg8H"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1Fi4hWc3LA9W9lpUQq-nVE92GuZzSaiNf"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=1XVvmUzHWoKEf1wwC6-OIThfHbwRix7oB"
            ]
        },

        "Maths Standard": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1z6V6imGdYMcE0ak78r19Hrjw--SVmQYF"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1nfwEcpbCVaQIGeHseCZKixwhFBy_6R91"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=1hdtrXVpckJ8R2wRLFtBlHIBqnviJPwyQ"
            ]
        },

        "Science": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1FxKeEUgvJVp8Qmh_FM-AxbTeM3no-Gkb"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1PlF5gmubQGXgZIsH-uIXuxxNzqb8rcHH"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=1ws3yd3dfAOF4jGWd6dUnJW7SFtSsL2CG"
            ]
        },

        "Social Science": {
            "2023-24": [
                "https://drive.google.com/uc?export=download&id=1aM-w9-dlTaUlhiKpJzojXapq_gILI44L"
            ],
            "2024-25": [
                "https://drive.google.com/uc?export=download&id=1awT8MtWR2t10LkhUdqDDJSM3dmGx_eYi"
            ],
            "2025-26": [
                "https://drive.google.com/uc?export=download&id=125r2C2O3JUuSnlQAqR2rJqhpp_VnA3M9"
            ]
        }
    },

    "11": {},
    "12": {}
}


# -------------------------
# Helper Functions
# -------------------------

def available_subjects_for_class(cls: str):
    return list(PAPERS.get(cls, {}).keys())

def available_years_for_subject(cls: str, subject: str):
    return sorted(PAPERS[cls][subject].keys(), reverse=True)

def papers_for(cls: str, subject: str, year: str):
    return PAPERS[cls][subject][year]


# -------------------------
# Bot Handlers
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to CBSE Question Paper Bot!\n"
        "Use /select_class to choose class."
    )

async def select_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for cls in ["9", "10", "11", "12"]:
        keyboard.append([InlineKeyboardButton(f"Class {cls}", callback_data=f"cls_{cls}")])

    await update.message.reply_text(
        "अपनी कक्षा चुनें:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_class_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    cls = query.data.split("_")[1]
    context.user_data["class"] = cls

    subjects = available_subjects_for_class(cls)
    if not subjects:
        await query.edit_message_text("इस कक्षा के लिए कोई subject उपलब्ध नहीं है।")
        return

    keyboard = [[InlineKeyboardButton(sub, callback_data=f"sub_{sub}")] for sub in subjects]

    await query.edit_message_text(
        f"Class {cls} — विषय चुनें:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_subject_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = query.data.split("_")[1]
    cls = context.user_data["class"]
    context.user_data["subject"] = subject

    years = available_years_for_subject(cls, subject)
    keyboard = [[InlineKeyboardButton(year, callback_data=f"yr_{year}")] for year in years]

    await query.edit_message_text(
        f"{subject} — Year चुनें:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_year_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    year = query.data.split("_")[1]
    cls = context.user_data["class"]
    subject = context.user_data["subject"]

    links = papers_for(cls, subject, year)

    await query.edit_message_text(
        f"Sending papers for Class {cls} — {subject} — {year}"
    )

    for idx, link in enumerate(links, start=1):
        try:
            await query.message.reply_document(
                document=link,
                filename=f"{subject}_{year}_{idx}.pdf",
                caption=f"{subject} {year} Paper {idx}"
            )
        except:
            await query.message.reply_text(f"Download link:\n{link}")


# -------------------------
# Main
# -------------------------

def main():
    TOKEN = os.getenv("7905996374:AAF5riYaLkzuf9EMXXxxRqTMtDUCiICRc4Y") or "7905996374:AAF5riYaLkzuf9EMXXxxRqTMtDUCiICRc4Y"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("select_class", select_class))

    app.add_handler(CallbackQueryHandler(handle_class_cb, pattern="^cls_"))
    app.add_handler(CallbackQueryHandler(handle_subject_cb, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(handle_year_cb, pattern="^yr_"))

    print("Bot is running…")
    app.run_polling()


if __name__ == "__main__":
    main()
