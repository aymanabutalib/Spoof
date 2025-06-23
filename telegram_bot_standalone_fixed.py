#!/usr/bin/env python3
"""
SpoofifyPro - Advanced Telegram Bot
A sophisticated Telegram bot for privacy and security services with multi-language support.

Author: SpoofifyPro Team
Contact: @Kawalgzaeery
Version: 1.0 - Fixed
"""

import logging
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================================
# CONFIGURATION
# ================================

# Replace with your bot token from @BotFather
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Data storage (in production, use a real database)
users_data: Dict[int, Dict] = {}
messages_data: List[Dict] = []
user_sessions: Dict[int, Dict] = {}

# ================================
# TRANSLATIONS
# ================================

TRANSLATIONS = {
    'ar': {
        'welcome': "🌍 يرجى اختيار لغتك المفضلة لبدء استخدام البوت:",
        'choose_language': "يرجى اختيار لغتك المفضلة للمتابعة:",
        'language_selected': "✅ تم اختيار اللغة العربية بنجاح!",
        'main_menu': "القائمة الرئيسية - اختر الخدمة المطلوبة:",
        'insufficient_balance': "💰 لا يمكن إتمام العملية لأن رصيدك غير كافٍ.\n\n⚠️ كل شيء مدفوع مسبقاً. لا توجد اشتراكات أو رسوم مخفية.",
        'virtual_number': "📱 رقم افتراضي مؤقت\nهاتف افتراضي / رقم ثاني\n\nرقم افتراضي لاستقبال المكالمات والرسائل عبر الويب، دون الحاجة لبطاقة SIM حقيقية.\nمناسب لحماية الخصوصية ❗\n\nاختر الدولة التي تريد الحصول على رقم منها 👇",
        'whats_sim': "🔢 Whats SIM\n\nرقم مؤقت يُستخدم لتفعيل خدمات مثل واتساب وتليجرام ولاين، دون الحاجة لبطاقة SIM فعلية. يمكنك أيضاً استقبال مكالمات ورسائل التفعيل عبر الصوت أو النص.\n\nاختر الدولة المطلوبة 👇",
        'payment_sent': "✅ تم إرسال الإشعار للدعم الفني. سيتم تفعيل رصيدك خلال دقائق بعد تأكيد المعاملة.",
        'back_to_menu': "🔙 العودة للقائمة الرئيسية",
        'balance_text': "💰 رصيدك الحالي: ${balance}\n\n{status}",
        'balance_low': "⚠️ رصيدك منخفض. يمكنك الشحن من القائمة الرئيسية.",
        'balance_sufficient': "✅ رصيدك كافٍ لاستخدام الخدمات.",
    },
    'en': {
        'welcome': "🌍 Please choose your preferred language to start using the bot:",
        'choose_language': "Please choose your preferred language to continue:",
        'language_selected': "✅ English language selected successfully!",
        'main_menu': "Main Menu - Choose the required service:",
        'insufficient_balance': "💰 The transaction cannot be completed because you have insufficient balance.\n\n⚠️ Everything is prepaid. No subscriptions or hidden fees.",
        'virtual_number': "📱 Temporary Virtual Number\nVirtual Phone / Second Number\n\nA virtual number to receive calls and messages via the web, without the need for a real SIM card.\nSuitable for privacy protection ❗\n\nChoose the country you want to get a number from 👇",
        'whats_sim': "🔢 Whats SIM\n\nA temporary number used to activate services such as WhatsApp, Telegram, and Line, without the need for a physical SIM card. You can also receive activation calls and messages via voice or text.\n\nSelect the desired country 👇",
        'payment_sent': "✅ Support team has been notified. Your balance will be activated within minutes after transaction confirmation.",
        'back_to_menu': "🔙 Back to Main Menu",
        'balance_text': "💰 Your current balance: ${balance}\n\n{status}",
        'balance_low': "⚠️ Your balance is low. You can top up from the main menu.",
        'balance_sufficient': "✅ Your balance is sufficient to use services.",
    },
    'fr': {
        'welcome': "🌍 Veuillez choisir votre langue préférée pour commencer à utiliser le bot:",
        'choose_language': "Veuillez choisir votre langue préférée pour continuer:",
        'language_selected': "✅ Langue française sélectionnée avec succès!",
        'main_menu': "Menu Principal - Choisissez le service requis:",
        'insufficient_balance': "💰 La transaction ne peut pas être complétée car votre solde est insuffisant.\n\n⚠️ Tout est prépayé. Pas d'abonnements ou de frais cachés.",
        'virtual_number': "📱 Numéro Virtuel Temporaire\nTéléphone Virtuel / Deuxième Numéro\n\nUn numéro virtuel pour recevoir des appels et des messages via le web, sans avoir besoin d'une vraie carte SIM.\nConvient pour la protection de la vie privée ❗\n\nChoisissez le pays d'où vous voulez obtenir un numéro 👇",
        'whats_sim': "🔢 Whats SIM\n\nUn numéro temporaire utilisé pour activer des services comme WhatsApp, Telegram et Line, sans avoir besoin d'une carte SIM physique.\n\nSélectionnez le pays désiré 👇",
        'payment_sent': "✅ L'équipe de support a été notifiée. Votre solde sera activé dans quelques minutes après confirmation de la transaction.",
        'back_to_menu': "🔙 Retour au Menu Principal",
        'balance_text': "💰 Votre solde actuel: ${balance}\n\n{status}",
        'balance_low': "⚠️ Votre solde est faible. Vous pouvez recharger depuis le menu principal.",
        'balance_sufficient': "✅ Votre solde est suffisant pour utiliser les services.",
    },
    'es': {
        'welcome': "🌍 Por favor elige tu idioma preferido para comenzar a usar el bot:",
        'choose_language': "Por favor elige tu idioma preferido para continuar:",
        'language_selected': "✅ ¡Idioma español seleccionado exitosamente!",
        'main_menu': "Menú Principal - Elige el servicio requerido:",
        'insufficient_balance': "💰 La transacción no se puede completar porque tienes saldo insuficiente.\n\n⚠️ Todo es prepago. Sin suscripciones o tarifas ocultas.",
        'virtual_number': "📱 Número Virtual Temporal\nTeléfono Virtual / Segundo Número\n\nUn número virtual para recibir llamadas y mensajes vía web, sin necesidad de una tarjeta SIM real.\nAdecuado para protección de privacidad ❗\n\nElige el país del que quieres obtener un número 👇",
        'whats_sim': "🔢 Whats SIM\n\nUn número temporal usado para activar servicios como WhatsApp, Telegram y Line, sin necesidad de una tarjeta SIM física.\n\nSelecciona el país deseado 👇",
        'payment_sent': "✅ El equipo de soporte ha sido notificado. Tu saldo será activado en minutos después de la confirmación de la transacción.",
        'back_to_menu': "🔙 Volver al Menú Principal",
        'balance_text': "💰 Tu saldo actual: ${balance}\n\n{status}",
        'balance_low': "⚠️ Tu saldo es bajo. Puedes recargar desde el menú principal.",
        'balance_sufficient': "✅ Tu saldo es suficiente para usar los servicios.",
    },
    'ru': {
        'welcome': "🌍 Пожалуйста, выберите предпочитаемый язык для начала использования бота:",
        'choose_language': "Пожалуйста, выберите предпочитаемый язык для продолжения:",
        'language_selected': "✅ Русский язык успешно выбран!",
        'main_menu': "Главное Меню - Выберите требуемую услугу:",
        'insufficient_balance': "💰 Транзакция не может быть завершена из-за недостаточного баланса.\n\n⚠️ Все предоплачено. Никаких подписок или скрытых комиссий.",
        'virtual_number': "📱 Временный Виртуальный Номер\nВиртуальный Телефон / Второй Номер\n\nВиртуальный номер для получения звонков и сообщений через веб, без необходимости в настоящей SIM-карте.\nПодходит для защиты конфиденциальности ❗\n\nВыберите страну, из которой хотите получить номер 👇",
        'whats_sim': "🔢 Whats SIM\n\nВременный номер, используемый для активации сервисов типа WhatsApp, Telegram и Line, без необходимости в физической SIM-карте.\n\nВыберите желаемую страну 👇",
        'payment_sent': "✅ Команда поддержки уведомлена. Ваш баланс будет активирован в течение нескольких минут после подтверждения транзакции.",
        'back_to_menu': "🔙 Назад в Главное Меню",
        'balance_text': "💰 Ваш текущий баланс: ${balance}\n\n{status}",
        'balance_low': "⚠️ Ваш баланс низкий. Вы можете пополнить из главного меню.",
        'balance_sufficient': "✅ Вашего баланса достаточно для использования услуг.",
    },
    'cn': {
        'welcome': "🌍 请选择您的首选语言开始使用机器人:",
        'choose_language': "请选择您的首选语言继续:",
        'language_selected': "✅ 中文语言选择成功!",
        'main_menu': "主菜单 - 选择所需服务:",
        'insufficient_balance': "💰 由于余额不足，无法完成交易。\n\n⚠️ 一切都是预付费的。没有订阅或隐藏费用。",
        'virtual_number': "📱 临时虚拟号码\n虚拟电话/第二号码\n\n通过网络接收电话和短信的虚拟号码，无需真实SIM卡。\n适合隐私保护 ❗\n\n选择您想要获取号码的国家 👇",
        'whats_sim': "🔢 Whats SIM\n\n用于激活WhatsApp、Telegram和Line等服务的临时号码，无需物理SIM卡。\n\n选择所需国家 👇",
        'payment_sent': "✅ 支持团队已收到通知。您的余额将在交易确认后几分钟内激活。",
        'back_to_menu': "🔙 返回主菜单",
        'balance_text': "💰 您的当前余额: ${balance}\n\n{status}",
        'balance_low': "⚠️ 您的余额较低。您可以从主菜单充值。",
        'balance_sufficient': "✅ 您的余额足以使用服务。",
    }
}

# ================================
# CRYPTO ADDRESSES
# ================================

CRYPTO_ADDRESSES = {
    'BTC': {
        'address': '3GvwS9tnSqp5hSKL5RquGKrxsR16quDdQv',
        'network': 'Bitcoin Network',
        'confirmations': 1,
        'price': 107198.37
    },
    'ETH': {
        'address': '0x2a3489047b085d04c8b9f8a2d7e3f1a6b8c9d0e1',
        'network': 'Ethereum (ERC20)',
        'confirmations': 12,
        'price': 3456.78
    },
    'USDT': {
        'address': 'TQn9Y2khEsLJW1ChVWFMSMeRDow5oREqjK',
        'network': 'TRC20 (Tron)',
        'confirmations': 1,
        'price': 1.0
    },
    'SOL': {
        'address': '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU',
        'network': 'Solana',
        'confirmations': 1,
        'price': 234.56
    },
    'LTC': {
        'address': 'LTC1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4',
        'network': 'Litecoin',
        'confirmations': 6,
        'price': 123.45
    },
    'DOGE': {
        'address': 'DH5yaieqoZN36fDVciNyRueRGvGLR3mr7L',
        'network': 'Dogecoin',
        'confirmations': 6,
        'price': 0.34
    },
    'BNB': {
        'address': '0x2a3489047b085d04c8b9f8a2d7e3f1a6b8c9d0e1',
        'network': 'BNB Smart Chain (BEP20)',
        'confirmations': 3,
        'price': 678.9
    }
}

# ================================
# MAIN BOT CLASS
# ================================

class SpoofifyProBot:
    def __init__(self):
        self.application = None
        
    def log_activity(self, action: str, user_id: int = 0, data: Any = None):
        """Log bot activities"""
        timestamp = datetime.now().isoformat()
        log_message = f"[{timestamp}] {action} - User: {user_id}"
        
        logger.info(log_message)
        if data:
            logger.info(f"Data: {json.dumps(data, default=str)}")
        
        # Store in messages_data
        messages_data.append({
            'timestamp': timestamp,
            'action': action,
            'user_id': user_id,
            'data': data
        })
        
        # Keep only last 1000 messages
        if len(messages_data) > 1000:
            messages_data[:] = messages_data[-1000:]

    def get_user_language(self, user_id: int) -> str:
        """Get user's selected language"""
        user = users_data.get(user_id, {})
        return user.get('selected_language', 'en')

    def get_translation(self, user_id: int, key: str) -> str:
        """Get translated text for user"""
        lang = self.get_user_language(user_id)
        return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))

    def update_user_data(self, user_id: int, user_info: Dict, **kwargs):
        """Update user data"""
        if user_id not in users_data:
            users_data[user_id] = {
                **user_info,
                'balance': 0,
                'selected_language': None,
                'join_date': datetime.now().isoformat(),
                'last_activity': datetime.now().isoformat(),
                'message_count': 0
            }
        
        users_data[user_id].update(kwargs)
        users_data[user_id]['last_activity'] = datetime.now().isoformat()
        users_data[user_id]['message_count'] = users_data[user_id].get('message_count', 0) + 1

    def get_user_balance(self, user_id: int) -> float:
        """Get user balance"""
        return users_data.get(user_id, {}).get('balance', 0)

    def update_user_balance(self, user_id: int, amount: float):
        """Update user balance"""
        if user_id in users_data:
            users_data[user_id]['balance'] = users_data[user_id].get('balance', 0) + amount
            self.log_activity("BALANCE_UPDATE", user_id, {
                'new_balance': users_data[user_id]['balance'],
                'added': amount
            })

    # ================================
    # KEYBOARD CREATORS
    # ================================

    def create_language_keyboard(self):
        """Create language selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🇸🇦 Arabic 🕌", callback_data="lang_ar"),
                InlineKeyboardButton("🇺🇸 English 🌐", callback_data="lang_en"),
                InlineKeyboardButton("🇫🇷 Français 🇫🇷", callback_data="lang_fr")
            ],
            [
                InlineKeyboardButton("🇪🇸 Español 🇪🇸", callback_data="lang_es"),
                InlineKeyboardButton("🇷🇺 Русский 🪆", callback_data="lang_ru"),
                InlineKeyboardButton("🇨🇳 中文 🇨🇳", callback_data="lang_cn")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_main_menu_keyboard(self):
        """Create main menu keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🕵️‍♂️ Spoof", callback_data="spoof"),
                InlineKeyboardButton("🔢 Whats SIM", callback_data="whats_sim")
            ],
            [
                InlineKeyboardButton("📱 Virtual Number", callback_data="virtual_number"),
                InlineKeyboardButton("💎 Top Up", callback_data="topup")
            ],
            [
                InlineKeyboardButton("🔍 Spokeo - Detect People", callback_data="spokeo"),
                InlineKeyboardButton("🛠️ Tools", callback_data="tools")
            ],
            [
                InlineKeyboardButton("ℹ️ Instructions and Support", callback_data="support")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_countries_keyboard(self, service_type="country"):
        """Create countries selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 America", callback_data=f"{service_type}_us"),
                InlineKeyboardButton("🇬🇧 Britain", callback_data=f"{service_type}_gb")
            ],
            [
                InlineKeyboardButton("🇩🇪 Germany", callback_data=f"{service_type}_de"),
                InlineKeyboardButton("🇸🇦 Saudi Arabia", callback_data=f"{service_type}_sa")
            ],
            [
                InlineKeyboardButton("🌍 Other countries", callback_data="other_countries")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_continents_keyboard(self):
        """Create continents selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🌎 North America", callback_data="continent_north_america"),
                InlineKeyboardButton("🌍 Europe", callback_data="continent_europe")
            ],
            [
                InlineKeyboardButton("🌏 Asia", callback_data="continent_asia"),
                InlineKeyboardButton("🌍 Africa", callback_data="continent_africa")
            ],
            [
                InlineKeyboardButton("🌐 Miscellaneous countries", callback_data="continent_misc")
            ],
            [
                InlineKeyboardButton("⬅️ Back", callback_data="back_virtual")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_continent_countries_keyboard(self, continent: str):
        """Create keyboard for countries in a specific continent"""
        countries_by_continent = {
            'north_america': [
                [
                    InlineKeyboardButton("🇺🇸 America", callback_data="country_us"),
                    InlineKeyboardButton("🇨🇦 Canada", callback_data="country_ca"),
                    InlineKeyboardButton("🇲🇽 Mexico", callback_data="country_mx")
                ],
                [
                    InlineKeyboardButton("🇵🇷 Puerto Rico", callback_data="country_pr"),
                    InlineKeyboardButton("🇵🇦 Panama", callback_data="country_pa"),
                    InlineKeyboardButton("🇯🇲 Jamaica", callback_data="country_jm")
                ]
            ],
            'europe': [
                [
                    InlineKeyboardButton("🇫🇷 France", callback_data="country_fr"),
                    InlineKeyboardButton("🇮🇹 Italy", callback_data="country_it"),
                    InlineKeyboardButton("🇪🇸 Spain", callback_data="country_es")
                ],
                [
                    InlineKeyboardButton("🇷🇺 Russia", callback_data="country_ru"),
                    InlineKeyboardButton("🇩🇪 Germany", callback_data="country_de"),
                    InlineKeyboardButton("🇹🇷 Turkey", callback_data="country_tr")
                ],
                [
                    InlineKeyboardButton("🇸🇪 Sweden", callback_data="country_se"),
                    InlineKeyboardButton("🇳🇴 Norway", callback_data="country_no"),
                    InlineKeyboardButton("🇫🇮 Finland", callback_data="country_fi")
                ]
            ],
            'asia': [
                [
                    InlineKeyboardButton("🇯🇵 Japan", callback_data="country_jp"),
                    InlineKeyboardButton("🇰🇷 South Korea", callback_data="country_kr"),
                    InlineKeyboardButton("🇨🇳 China", callback_data="country_cn")
                ],
                [
                    InlineKeyboardButton("🇮🇳 India", callback_data="country_in"),
                    InlineKeyboardButton("🇮🇩 Indonesia", callback_data="country_id"),
                    InlineKeyboardButton("🇵🇭 Philippines", callback_data="country_ph")
                ],
                [
                    InlineKeyboardButton("🇦🇪 UAE", callback_data="country_ae"),
                    InlineKeyboardButton("🇶🇦 Qatar", callback_data="country_qa"),
                    InlineKeyboardButton("🇰🇼 Kuwait", callback_data="country_kw")
                ]
            ],
            'africa': [
                [
                    InlineKeyboardButton("🇪🇬 Egypt", callback_data="country_eg"),
                    InlineKeyboardButton("🇲🇦 Morocco", callback_data="country_ma"),
                    InlineKeyboardButton("🇩🇿 Algeria", callback_data="country_dz")
                ],
                [
                    InlineKeyboardButton("🇳🇬 Nigeria", callback_data="country_ng"),
                    InlineKeyboardButton("🇿🇦 South Africa", callback_data="country_za"),
                    InlineKeyboardButton("🇹🇳 Tunisia", callback_data="country_tn")
                ]
            ],
            'misc': [
                [
                    InlineKeyboardButton("🇦🇺 Australia", callback_data="country_au"),
                    InlineKeyboardButton("🇳🇿 New Zealand", callback_data="country_nz"),
                    InlineKeyboardButton("🇮🇱 Israel", callback_data="country_il")
                ],
                [
                    InlineKeyboardButton("🇧🇷 Brazil", callback_data="country_br"),
                    InlineKeyboardButton("🇦🇷 Argentina", callback_data="country_ar"),
                    InlineKeyboardButton("🇨🇱 Chile", callback_data="country_cl")
                ]
            ]
        }
        
        keyboard = countries_by_continent.get(continent, [])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="other_countries")])
        
        return InlineKeyboardMarkup(keyboard)

    def create_insufficient_balance_keyboard(self):
        """Create insufficient balance keyboard"""
        keyboard = [
            [InlineKeyboardButton("💎 Top up your balance", callback_data="topup")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_topup_keyboard(self):
        """Create top-up amounts keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("$50", callback_data="topup_50"),
                InlineKeyboardButton("$100", callback_data="topup_100"),
                InlineKeyboardButton("$200", callback_data="topup_200")
            ],
            [
                InlineKeyboardButton("$300", callback_data="topup_300"),
                InlineKeyboardButton("$500", callback_data="topup_500"),
                InlineKeyboardButton("$1000", callback_data="topup_1000")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_crypto_keyboard(self):
        """Create cryptocurrency selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("BTC", callback_data="crypto_BTC"),
                InlineKeyboardButton("ETH", callback_data="crypto_ETH"),
                InlineKeyboardButton("USDT", callback_data="crypto_USDT")
            ],
            [
                InlineKeyboardButton("SOL", callback_data="crypto_SOL"),
                InlineKeyboardButton("LTC", callback_data="crypto_LTC"),
                InlineKeyboardButton("DOGE", callback_data="crypto_DOGE")
            ],
            [InlineKeyboardButton("BNB", callback_data="crypto_BNB")],
            [InlineKeyboardButton("🔙 Back", callback_data="topup")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_payment_keyboard(self):
        """Create payment confirmation keyboard"""
        keyboard = [
            [InlineKeyboardButton("✅ Amount sent", callback_data="payment_sent")],
            [InlineKeyboardButton("🔙 Return", callback_data="topup")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_spoof_keyboard(self):
        """Create spoof services keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📱 Fake SMS", callback_data="spoof_sms"),
                InlineKeyboardButton("📞 Fake Call", callback_data="spoof_call")
            ],
            [
                InlineKeyboardButton("🎭 Caller ID Spoof", callback_data="spoof_caller_id"),
                InlineKeyboardButton("📧 Email Spoof", callback_data="spoof_email")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_spokeo_keyboard(self):
        """Create Spokeo services keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("🔎 People Search", callback_data="spokeo_people"),
                InlineKeyboardButton("☎️ Search by Phone Number", callback_data="spokeo_phone")
            ],
            [
                InlineKeyboardButton("📄 Criminal and Court Records", callback_data="spokeo_criminal"),
                InlineKeyboardButton("🌐 OSINT and Additional Features", callback_data="spokeo_osint")
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_tools_keyboard(self):
        """Create tools keyboard"""
        keyboard = [
            [
                InlineKeyboardButton("📱 Trash Mobile", callback_data="tool_trash_mobile"),
                InlineKeyboardButton("📧 Trash Mail", callback_data="tool_trash_mail")
            ],
            [
                InlineKeyboardButton("📞 Call Forward", callback_data="tool_call_forward"),
                InlineKeyboardButton("📲 Phone Checker", callback_data="tool_phone_checker")
            ],
            [
                InlineKeyboardButton("📡 HLR Lookup", callback_data="tool_hlr"),
                InlineKeyboardButton("🔍 Find Caller Name", callback_data="tool_cnam")
            ],
            [
                InlineKeyboardButton("🖼️ Image Editor", callback_data="tool_image_editor"),
                InlineKeyboardButton("🕵️ Stalk Scan", callback_data="tool_stalk_scan")
            ],
            [InlineKeyboardButton("🧾 Fake Data", callback_data="tool_fake_data")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_support_keyboard(self):
        """Create support keyboard"""
        keyboard = [
            [InlineKeyboardButton("📩 Message Support", url="https://t.me/Kawalgzaeery")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    # ================================
    # COMMAND HANDLERS
    # ================================

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        self.log_activity("START_COMMAND", user_id)
        
        # Update user data
        self.update_user_data(user_id, {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        })
        
        # Check if user has selected language
        if not users_data.get(user_id, {}).get('selected_language'):
            await self.show_language_selection(update, context)
        else:
            await self.show_main_menu(update, context)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        self.log_activity("HELP_COMMAND", user_id)
        
        lang = self.get_user_language(user_id)
        
        help_texts = {
            'ar': """ℹ️ <b>المساعدة والأسئلة الشائعة</b>

مرحباً بك في <b>SpoofifyPro</b> 👋
إليك دليلك السريع لاستخدام الخدمات المتاحة:

—

<b>📱 رقم افتراضي مؤقت</b>
استخدم رقماً حقيقياً بدون بطاقة SIM لتفعيل الخدمات أو استقبال المكالمات والرسائل.

<b>🔢 Whats SIM</b>
رقم افتراضي مخصص لتفعيل واتساب وتليجرام وغيرها بالرسائل أو المكالمات الصوتية.

<b>🛠️ أدوات متقدمة</b>
مثل: فحص الأرقام، HLR، هوية المتصل، مولد البيانات الوهمية، والمزيد.

<b>🔍 Spokeo</b>
أداة قوية للبحث عن الأشخاص بالاسم أو البريد الإلكتروني أو الرقم أو العنوان.

<b>🕵️‍♂️ Spoof</b>
خدمات التزييف: إرسال SMS مزيف، مكالمات مزيفة، تغيير هوية المتصل، والمزيد.

<b>💎 شحن رصيدك</b>
اختر مبلغ الشحن واختر العملة الرقمية، واستلم العنوان للدفع.

—

<b>❓ هل يوجد اشتراك شهري؟</b>
لا. جميع الخدمات مدفوعة مسبقاً فقط.
❌ لا توجد رسوم مخفية — ❌ لا توجد اشتراكات.

<b>💰 نفد الرصيد؟</b>
ستتلقى رسالة تلقائية مع الخيارات التالية:
<code>💎 شحن رصيدك</code> أو <code>🔙 العودة</code>

—

<b>📞 الدعم الفني:</b>
راسلنا عبر: <a href="https://t.me/Kawalgzaeery">@Kawalgzaeery</a>

—

⚠️ قد لا تُستخدم الخدمات لأغراض غير قانونية.
مصممة للخصوصية والمزح والاختبار وأغراض الأمان فقط ✅""",
            
            'en': """ℹ️ <b>Help and FAQ</b>

Welcome to <b>SpoofifyPro</b> 👋
Here's your quick guide to using the available services:

—

<b>📱 Temporary Virtual Number</b>
Use a real number without a SIM card to activate services or receive calls and messages.

<b>🔢 Whats SIM</b>
A virtual number dedicated to activating WhatsApp, Telegram, and others with messages or voice calls.

<b>🛠️ Advanced Tools</b>
Such as: Number Check, HLR, Caller ID, Fake Data Generator, and more.

<b>🔍 Spokeo</b>
A powerful tool to search for people by name, email, number, or address.

<b>🕵️‍♂️ Spoof</b>
Spoofing Services: Sending Fake SMS, Fake Calls, Changing Caller ID, and more.

<b>💎 Top-up Your Balance</b>
Choose the top-up amount and select the digital currency, and receive the address for payment.

—

<b>❓ Is there a monthly subscription?</b>
No. All services are prepaid only.
❌ No hidden fees — ❌ No subscriptions.

<b>💰 Ran out of credit?</b>
You will receive an automatic message with the following options:
<code>💎 Top up your credit</code> or <code>🔙 Return</code>

—

<b>📞 Technical Support:</b>
Message us via: <a href="https://t.me/Kawalgzaeery">@Kawalgzaeery</a>

—

⚠️ The services may not be used for illegal purposes.
Designed for privacy, pranks, testing, and security purposes only ✅"""
        }
        
        help_text = help_texts.get(lang, help_texts['en'])
        await update.message.reply_text(help_text, parse_mode='HTML', disable_web_page_preview=True)

    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /balance command"""
        user_id = update.effective_user.id
        self.log_activity("BALANCE_COMMAND", user_id)
        
        balance = self.get_user_balance(user_id)
        status = self.get_translation(user_id, 'balance_low' if balance < 50 else 'balance_sufficient')
        
        balance_text = self.get_translation(user_id, 'balance_text').format(
            balance=balance,
            status=status
        )
        
        await update.message.reply_text(balance_text)

    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        user_id = update.effective_user.id
        self.log_activity("MENU_COMMAND", user_id)
        
        await self.show_main_menu(update, context)

    # ================================
    # MENU DISPLAY FUNCTIONS
    # ================================

    async def show_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show language selection menu"""
        keyboard = self.create_language_keyboard()
        text = "🌍 Please choose your preferred language to start using the bot:\n\nPlease choose your preferred language to continue:"
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text, reply_markup=keyboard)

    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, edit_message=False):
        """Show main menu"""
        user_id = update.effective_user.id
        keyboard = self.create_main_menu_keyboard()
        text = self.get_translation(user_id, 'main_menu')
        
        if edit_message and update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
        elif update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
        else:
            await update.message.reply_text(text, reply_markup=keyboard)

    async def show_virtual_number_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show virtual number menu"""
        user_id = update.effective_user.id
        keyboard = self.create_countries_keyboard("country")
        text = self.get_translation(user_id, 'virtual_number')
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_whats_sim_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show WhatsApp SIM menu"""
        user_id = update.effective_user.id
        keyboard = self.create_countries_keyboard("whats_country")
        text = self.get_translation(user_id, 'whats_sim')
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_insufficient_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show insufficient balance message"""
        user_id = update.effective_user.id
        keyboard = self.create_insufficient_balance_keyboard()
        text = self.get_translation(user_id, 'insufficient_balance')
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_topup_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show top-up menu"""
        user_id = update.effective_user.id
        keyboard = self.create_topup_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': "💰 تجديد الرصيد\n\nيرجى كتابة أو اختيار المبلغ الذي تريد شحنه (بالدولار).\n🔻 الحد الأدنى للشحن: $50",
            'en': "💰 Renewal\n\nPlease type or select the amount you want to top up (in dollars).\n🔻 Minimum top-up: $50"
        }.get(lang, "💰 Renewal\n\nPlease type or select the amount you want to top up (in dollars).\n🔻 Minimum top-up: $50")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_crypto_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, amount: str):
        """Show cryptocurrency selection"""
        user_id = update.effective_user.id
        keyboard = self.create_crypto_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': f"✅ المبلغ المحدد: ${amount}\n\n🔜 الآن اختر العملة التي تريد الدفع بها:\n\n💱 ₿ العملات المشفرة\n\nاختر العملة التي تريد الدفع بها:\n👇 اضغط على العملة:",
            'en': f"✅ Amount selected: ${amount}\n\n🔜 Now choose the currency you want to pay with:\n\n💱 ₿ Cryptocurrencies\n\nChoose the currency you want to pay with:\n👇 Click on the currency:"
        }.get(lang, f"✅ Amount selected: ${amount}\n\n🔜 Now choose the currency you want to pay with:\n\n💱 ₿ Cryptocurrencies\n\nChoose the currency you want to pay with:\n👇 Click on the currency:")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_payment_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE, amount: str, crypto: str):
        """Show payment details"""
        user_id = update.effective_user.id
        keyboard = self.create_payment_keyboard()
        
        # Store crypto selection in session
        if user_id not in user_sessions:
            user_sessions[user_id] = {}
        user_sessions[user_id]['selected_crypto'] = crypto
        user_sessions[user_id]['selected_amount'] = amount
        
        crypto_info = CRYPTO_ADDRESSES[crypto]
        address = crypto_info['address']
        network = crypto_info['network']
        price = crypto_info['price']
        
        # Calculate crypto amount
        crypto_amount = round(float(amount) / price, 8)
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': f"""💰 تجديد الرصيد

✅ طريقة الدفع: {crypto}
🌐 الشبكة: {network}
💵 المبلغ: ${amount}

📤 أرسل إلى العنوان أدناه:

<code>{address}</code>

💸 القيمة المطلوبة: {crypto_amount} {crypto}
📊 (سعر الصرف الحالي: ${price:,.2f})

⏳ العنوان صالح لمدة ساعة واحدة.
⚠️ قد يختلف المبلغ قليلاً بسبب تقلبات الأسعار.

🔔 بعد الإرسال، اضغط "تم الإرسال" وسيتم تفعيل رصيدك تلقائياً.""",
            'en': f"""💰 Renewal

✅ Payment Method: {crypto}
🌐 Network: {network}
💵 Amount: ${amount}

📤 Send to the address below:

<code>{address}</code>

💸 Requested Value: {crypto_amount} {crypto}
📊 (Current Exchange Rate: ${price:,.2f})

⏳ Address valid for 1 hour.
⚠️ Amount may vary slightly due to price fluctuations.

🔔 After sending, click "Amount sent" and your balance will be activated automatically."""
        }.get(lang, f"""💰 Renewal

✅ Payment Method: {crypto}
🌐 Network: {network}
💵 Amount: ${amount}

📤 Send to the address below:

<code>{address}</code>

💸 Requested Value: {crypto_amount} {crypto}
📊 (Current Exchange Rate: ${price:,.2f})

⏳ Address valid for 1 hour.
⚠️ Amount may vary slightly due to price fluctuations.

🔔 After sending, click "Amount sent" and your balance will be activated automatically.""")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard, parse_mode='HTML')

    async def show_spoof_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show spoof services menu"""
        user_id = update.effective_user.id
        keyboard = self.create_spoof_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': "🕵️‍♂️ خدمات التزييف\n\nاختر خدمة التزييف التي تريد استخدامها:\n\n• رسائل SMS مزيفة - إرسال رسائل نصية مزيفة\n• مكالمات مزيفة - إجراء مكالمات هاتفية مزيفة\n• تزييف هوية المتصل - تغيير هوية المتصل\n• بريد إلكتروني مزيف - إرسال رسائل بريد إلكتروني مزيفة",
            'en': "🕵️‍♂️ Spoof Services\n\nChoose the spoofing service you want to use:\n\n• Fake SMS - Send fake text messages\n• Fake Call - Make fake phone calls\n• Caller ID Spoof - Change your caller ID\n• Email Spoof - Send spoofed emails"
        }.get(lang, "🕵️‍♂️ Spoof Services\n\nChoose the spoofing service you want to use:\n\n• Fake SMS - Send fake text messages\n• Fake Call - Make fake phone calls\n• Caller ID Spoof - Change your caller ID\n• Email Spoof - Send spoofed emails")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_spokeo_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show Spokeo menu"""
        user_id = update.effective_user.id
        keyboard = self.create_spokeo_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': """🔍 Spokeo - خدمة تحديد الهوية المتقدمة

📌 وصف الخدمة:
Spokeo هو أداة بحث قوية تتيح لك جمع المعلومات الشخصية والعامة عن الأفراد بالاسم أو رقم الهاتف أو البريد الإلكتروني أو العنوان.

✅ النتائج تشمل:
• معلومات الاتصال وأفراد العائلة والمواقع السكنية وحسابات وسائل التواصل الاجتماعي.
• السجلات التاريخية والجنائية وقيم العقارات.
• نتائج سريعة مع دعم فني وخصوصية صارمة.

⚠️ ملاحظة:
لا يُستخدم للأغراض القانونية (مثل التوظيف أو الإيجار)، وقد تكون بعض البيانات غير دقيقة وفقاً لـ FCRA.""",
            'en': """🔍 Spokeo - Advanced Person Identification Service

📌 Service Description:
Spokeo is a powerful search tool that allows you to gather personal and general information about individuals by name, phone number, email, or address.

✅ Results include:
• Contact information, family members, residential locations, and social media accounts.
• Historical and criminal records, and real estate values.
• Fast results, with technical support and strict privacy.

⚠️ Note:
Not to be used for legal purposes (such as employment or rental), and some data may be inaccurate according to the FCRA."""
        }.get(lang, """🔍 Spokeo - Advanced Person Identification Service

📌 Service Description:
Spokeo is a powerful search tool that allows you to gather personal and general information about individuals by name, phone number, email, or address.

✅ Results include:
• Contact information, family members, residential locations, and social media accounts.
• Historical and criminal records, and real estate values.
• Fast results, with technical support and strict privacy.

⚠️ Note:
Not to be used for legal purposes (such as employment or rental), and some data may be inaccurate according to the FCRA.""")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_tools_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show tools menu"""
        user_id = update.effective_user.id
        keyboard = self.create_tools_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': "🛠️ الأدوات المتقدمة المتاحة:\n\n⬇️ اختر الأداة التي تريد عرض تفاصيلها:",
            'en': "🛠️ Available Advanced Tools:\n\n⬇️ Choose the tool you want to view details for:"
        }.get(lang, "🛠️ Available Advanced Tools:\n\n⬇️ Choose the tool you want to view details for:")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_support_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show support menu"""
        user_id = update.effective_user.id
        keyboard = self.create_support_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': f"""ℹ️ تعليمات المستخدم والدعم

📘 هذا دليل بسيط لاستخدام أبرز خدمات البوت:

📱 رقم افتراضي
اختر دولتك، ثم استقبل المكالمات أو الرسائل باستخدام رقم رقمي مؤقت.

🔢 Whats SIM
أرقام لتفعيل واتساب/تليجرام بدون SIM فعلية، بما في ذلك استقبال المكالمات والرسائل.

🛠️ الأدوات
أدوات متنوعة مثل Trash Mail وفحص الأرقام وCNAM وتحرير الصور وتوليد بيانات وهمية والمزيد.

🔍 Spokeo
البحث عن الأشخاص بالاسم أو الرقم أو البريد الإلكتروني. يشمل التقارير العامة والهويات وجهات الاتصال.

💎 شحن الرصيد
شحن رصيدك بالدولار باستخدام العملات المشفرة. الحد الأدنى 50 دولار والدفع تلقائي.

📞 للتواصل مع الدعم الفني:
👤 تليجرام: @Kawalgzaeery""",
            'en': f"""ℹ️ User Instructions & Support

📘 This is a simple guide to using the bot's most prominent services:

📱 Virtual Number
Choose your country, then receive calls or messages using a temporary digital number.

🔢 Whats SIM
Numbers to activate WhatsApp/Telegram without a physical SIM, including receiving calls and messages.

🛠️ Tools
Various tools such as Trash Mail, number check, CNAM, image editing, generating fake data, and more.

🔍 Spokeo
Search for people by name, number, or email. Includes general reports, identities, and contacts.

💎 Top Up Your Balance
Top up your balance in dollars using cryptocurrencies. The minimum is $50, and payment is automatic.

📞 To contact technical support:
👤 Telegram: @Kawalgzaeery"""
        }.get(lang, f"""ℹ️ User Instructions & Support

📘 This is a simple guide to using the bot's most prominent services:

📱 Virtual Number
Choose your country, then receive calls or messages using a temporary digital number.

🔢 Whats SIM
Numbers to activate WhatsApp/Telegram without a physical SIM, including receiving calls and messages.

🛠️ Tools
Various tools such as Trash Mail, number check, CNAM, image editing, generating fake data, and more.

🔍 Spokeo
Search for people by name, number, or email. Includes general reports, identities, and contacts.

💎 Top Up Your Balance
Top up your balance in dollars using cryptocurrencies. The minimum is $50, and payment is automatic.

📞 To contact technical support:
👤 Telegram: @Kawalgzaeery""")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_continents_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show continents menu"""
        user_id = update.effective_user.id
        keyboard = self.create_continents_keyboard()
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': "🌍 اختر قارة لعرض الدول المتاحة:",
            'en': "🌍 Select a continent to view available countries:"
        }.get(lang, "🌍 Select a continent to view available countries:")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    async def show_countries_by_continent(self, update: Update, context: ContextTypes.DEFAULT_TYPE, continent: str):
        """Show countries by continent"""
        user_id = update.effective_user.id
        keyboard = self.create_continent_countries_keyboard(continent)
        
        lang = self.get_user_language(user_id)
        text = {
            'ar': "🌍 اختر دولة:",
            'en': "🌍 Select a country:"
        }.get(lang, "🌍 Select a country:")
        
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)

    # ================================
    # CALLBACK QUERY HANDLER
    # ================================

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callback queries"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        self.log_activity("CALLBACK_RECEIVED", user_id, {'data': data})
        
        # Language selection
        if data.startswith("lang_"):
            selected_lang = data.replace("lang_", "")
            users_data[user_id]['selected_language'] = selected_lang
            self.log_activity("LANGUAGE_SELECTED", user_id, {'language': selected_lang})
            
            await query.edit_message_text(self.get_translation(user_id, 'language_selected'))
            await asyncio.sleep(1.5)
            await self.show_main_menu(update, context, edit_message=True)
        
        # Main menu selections
        elif data == "virtual_number":
            await self.show_virtual_number_menu(update, context)
        elif data == "whats_sim":
            await self.show_whats_sim_menu(update, context)
        elif data == "spoof":
            await self.show_spoof_menu(update, context)
        elif data == "spokeo":
            await self.show_spokeo_menu(update, context)
        elif data == "tools":
            await self.show_tools_menu(update, context)
        elif data == "topup":
            await self.show_topup_menu(update, context)
        elif data == "support":
            await self.show_support_menu(update, context)
        
        # Navigation
        elif data == "other_countries":
            await self.show_continents_menu(update, context)
        elif data.startswith("continent_"):
            continent = data.replace("continent_", "")
            await self.show_countries_by_continent(update, context, continent)
        
        # Country selections (show insufficient balance)
        elif data.startswith("country_") or data.startswith("whats_country_"):
            await self.show_insufficient_balance(update, context)
        
        # Top-up flow
        elif data.startswith("topup_"):
            amount = data.replace("topup_", "")
            if user_id not in user_sessions:
                user_sessions[user_id] = {}
            user_sessions[user_id]['selected_amount'] = amount
            await self.show_crypto_selection(update, context, amount)
        elif data.startswith("crypto_"):
            crypto = data.replace("crypto_", "")
            session = user_sessions.get(user_id, {})
            if session.get('selected_amount'):
                await self.show_payment_details(update, context, session['selected_amount'], crypto)
        
        # Payment confirmation
        elif data == "payment_sent":
            session = user_sessions.get(user_id, {})
            if session.get('selected_amount'):
                self.log_activity("PAYMENT_REPORTED", user_id, session)
                await query.edit_message_text(self.get_translation(user_id, 'payment_sent'))
        
        # Service selections (show insufficient balance for all)
        elif (data.startswith("spoof_") or data.startswith("spokeo_") or 
              data.startswith("tool_")):
            await self.show_insufficient_balance(update, context)
        
        # Back buttons
        elif data == "back_main":
            await self.show_main_menu(update, context, edit_message=True)
        elif data == "back_virtual":
            await self.show_virtual_number_menu(update, context)
        elif data == "back_whats":
            await self.show_whats_sim_menu(update, context)

    # ================================
    # BOT SETUP AND RUN
    # ================================

    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))

    async def run_bot(self):
        """Run the bot"""
        if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ Please set your bot token in the BOT_TOKEN variable!")
            logger.error("Get your token from @BotFather on Telegram")
            return
        
        logger.info("🚀 Starting SpoofifyPro Bot...")
        
        # Create application
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Log startup
        self.log_activity("BOT_STARTED", 0, {"version": "1.0"})
        
        logger.info("✅ SpoofifyPro Bot is running!")
        logger.info("📱 Send /start to your bot to begin")
        logger.info("🛑 Press Ctrl+C to stop the bot")
        
        # Run the bot
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ================================
# MAIN EXECUTION
# ================================

async def main():
    """Main async function"""
    print("🌟 SpoofifyPro - Advanced Telegram Bot")
    print("=" * 50)
    print("🔧 Initializing bot...")
    
    bot = SpoofifyProBot()
    await bot.run_bot()

def run_main():
    """Run the main function"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
        logger.info("Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == "__main__":
    run_main()
