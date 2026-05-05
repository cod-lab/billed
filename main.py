from fastapi import Request, Depends, HTTPException

from pprint import pprint as pp

from .backend.core.config import get_settings
from .backend.utils.mongodb import MongoDB
from .server_template import Server


# GETTING ENV VARS
settings = get_settings()


# ******** SETUP SERVER ********
server = Server()

app = server.create_app(    # creating var 'app' for main.py file as it searches only for var 'app' to run the server
    debug = settings.debug,
    title = settings.title,
    description = settings.description,
    version = settings.version,
    lifespan = {    # for mongo db connectivity
        'on_startup_fnc': MongoDB.startup,
        'on_shutdown_fnc': MongoDB.shutdown,
    }
)

# HTML files path
server.set_templates_path(settings.templates_path)

# STATIC files path (js, css, img, etc.)
server.mount_assets(
    assets_url = settings.assets_url,
    assets_path = settings.assets_path,
    assets_app_name = settings.assets_app_name
)
# ******** ************ ********



# CHECKING DB Connection
@app.get("/check_db_con")
async def check_db(db = Depends(MongoDB.get_db)):
    """
    Injecting db dependency 'MongoDB.get_db' into function 'check_db' using 'Depends' using var 'db'.
    Depends automatically calls the fnc 'MongoDB.get_db' and pass the arg 'request' to it.
    """
    try:
        await db.command("ping")
        return {"status": "MongoDB connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# SERVING HOME TEMPLATE
@app.get('/')
def home(request: Request):
    from .forms_and_fields import (
        supplier_details,
        invoice_details,
        buyer_details,
        product_details,
        dispatch_details,
        payment_details
    )

    # pp(products_details)

    return server.serve_template(request, "home.html", {
        "default_theme": "dark",
        "forms": [
            {
                "form_class": "buyer_details",
                "form_id": "buyer_form",
                "form_heading": "buyer details",
                "form_fields": buyer_details,
                "form_api": "/buyer_details"
            },
            {
                "form_class": "products_details",
                "form_id": "products_form",
                "form_heading": "products details",
                "form_fields": product_details,
                "form_api": "/products_details"
            },
            {
                "form_class": "invoice_details",
                "form_id": "invoice_form",
                "form_heading": "invoice details",
                "form_fields": invoice_details,
                "form_api": "/invoice_details"
            },
            {
                "form_class": "dispatch_details",
                "form_id": "dispatch_form",
                "form_heading": "dispatch details",
                "form_fields": dispatch_details,
                "form_api": "/dispatch_details"
            },
            {
                "form_class": "payment_details",
                "form_id": "payment_form",
                "form_heading": "payment details",
                "form_fields": payment_details,
                "form_api": "/payment_details"
            },
            {
                "form_class": "supplier_details",
                "form_id": "supplier_form",
                "form_heading": "supplier details",
                "form_fields": supplier_details,
                "form_api": "/supplier_details"
            },
        ],
        "buttons": {
            "theme_buttons": [
                {
                    "label": "☀️ Light",
                    "type": "button",
                    "onclick_fnc": "set_theme",
                    "mode": "light"
                },
                {
                    "label": "🌙 Dark",
                    "type": "button",
                    "onclick_fnc": "set_theme",
                    "mode": "dark"
                },
            ],
            "submit_button": {
                "label": "Generate Invoice",
                "type": "button",
                "onclick_fnc": "submit_all_forms",
            }
        },
    })


