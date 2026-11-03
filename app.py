import os
import csv
import io
import hmac
import secrets
from datetime import datetime, timezone, timedelta
from functools import wraps

from dotenv import load_dotenv
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, abort, make_response, session
)
from werkzeug.security import check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from supabase import create_client

load_dotenv()

# --------------------------------------------------
# FLASK CONFIGURATION
# --------------------------------------------------

app = Flask(__name__, static_folder="public", static_url_path="/static")

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "")

if os.getenv("VERCEL") and not SECRET_KEY:
    raise RuntimeError(
        "FLASK_SECRET_KEY must be configured in Vercel Environment Variables."
    )

app.secret_key = SECRET_KEY or "local-development-only-change-me"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "true").lower() == "true",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
)

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1
)

# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "919000000000")
PHONE_DISPLAY = os.getenv("PHONE_DISPLAY", "+91 90000 00000")
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:5000")

supabase = None

if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )

# --------------------------------------------------
# WEBSITE DATA
# --------------------------------------------------

PRODUCTS = [
    {
        "slug": "bwp-plywood",
        "name": "Kohinoor Gold",
        "grade": "BWP · IS 710*",
        "category": "Plywood",
        "desc": "A dependable choice for demanding spaces where moisture resistance matters.",
        "best": "Kitchens, utility areas and high-use interiors",
        "thickness": "6, 8, 12, 16, 19, 25 mm",
        "warranty": "Up to 21 years*",
        "badge": "Flagship range",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "bwr-plywood",
        "name": "Kohinoor Premium",
        "grade": "BWR · IS 303*",
        "category": "Plywood",
        "desc": "A versatile grade for everyday interior applications with occasional moisture exposure.",
        "best": "Kitchens, wardrobes and furniture",
        "thickness": "6, 8, 12, 16, 19, 25 mm",
        "warranty": "7–15 years*",
        "badge": "Everyday performance",
        "image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "mr-plywood",
        "name": "Kohinoor Classic",
        "grade": "MR · IS 303*",
        "category": "Plywood",
        "desc": "A practical interior-grade option for dry areas and general furniture work.",
        "best": "Bedrooms, wardrobes and living spaces",
        "thickness": "6, 8, 12, 16, 19, 25 mm",
        "warranty": "7–15 years*",
        "badge": "Interior essential",
        "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "calibrated-plywood",
        "name": "Calibrated Plywood",
        "grade": "Uniform thickness",
        "category": "Plywood",
        "desc": "Consistent thickness for cleaner fabrication and a smooth finished surface.",
        "best": "Modular furniture and precision interiors",
        "thickness": "Available options: confirm with team",
        "warranty": "Confirm by grade",
        "badge": "Precision finish",
        "image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "marine-plywood",
        "name": "Marine Plywood",
        "grade": "Marine grade",
        "category": "Plywood",
        "desc": "A plywood option for applications requiring enhanced moisture performance.",
        "best": "Specified wet-area and marine applications",
        "thickness": "Ask for available sizes",
        "warranty": "Confirm by product",
        "badge": "Specialist application",
        "image": "https://images.unsplash.com/photo-1600607687644-c7171b42498f?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "flexible-plywood",
        "name": "Flexible Plywood",
        "grade": "Bendable panels",
        "category": "Plywood",
        "desc": "Designed for curved forms and rounded furniture details.",
        "best": "Curved counters, columns and furniture",
        "thickness": "Ask for available sizes",
        "warranty": "Confirm by product",
        "badge": "Design flexibility",
        "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "shuttering-plywood",
        "name": "Kohinoor Shield",
        "grade": "Film-faced",
        "category": "Plywood",
        "desc": "A shuttering range for construction and formwork requirements.",
        "best": "Concrete formwork and construction",
        "thickness": "Ask for available sizes",
        "warranty": "Confirm by product",
        "badge": "For construction",
        "image": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "blockboards",
        "name": "Block Boards & Flush Doors",
        "grade": "19 & 25 mm options",
        "category": "Boards & Doors",
        "desc": "Stable board solutions and flush doors, including teak veneer options.",
        "best": "Doors, long-span shelves and furniture",
        "thickness": "19, 25 mm block boards",
        "warranty": "Confirm by product",
        "badge": "Doors & boards",
        "image": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "laminates-veneers",
        "name": "Laminates & Veneers",
        "grade": "Decorative surfaces",
        "category": "Surfaces",
        "desc": "A considered collection of laminates and natural veneers for finished spaces.",
        "best": "Cabinet fronts, furniture and wall panels",
        "thickness": "Laminates: 0.8, 1.0, 1.25 mm",
        "warranty": "Confirm by collection",
        "badge": "Finishing touches",
        "image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "timber-mdf-hdhmr",
        "name": "Timber, MDF & Boards",
        "grade": "Multiple materials",
        "category": "Boards & Timber",
        "desc": "Teak, sal and pine timber, MDF, HDHMR and particle board options.",
        "best": "Interior fit-outs and furniture manufacturing",
        "thickness": "Ask for available sizes",
        "warranty": "Varies by material",
        "badge": "One-stop sourcing",
        "image": "https://images.unsplash.com/photo-1600210492493-0946911123ea?auto=format&fit=crop&w=1200&q=85"
    },
    {
        "slug": "hardware",
        "name": "Hardware & Accessories",
        "grade": "Project essentials",
        "category": "Hardware",
        "desc": "Adhesives, hinges, channels, locks and handles for a complete material order.",
        "best": "Furniture installation and fit-outs",
        "thickness": "Multiple options",
        "warranty": "Varies by brand",
        "badge": "Finishing essentials",
        "image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=1200&q=85"
    }
]

CITIES = [
    "Mumbai", "Thane", "Navi Mumbai", "Kalyan",
    "Vasai-Virar", "Pune", "Nashik", "Nagpur", "Aurangabad"
]

CATEGORIES = [
    "Plywood", "Boards & Doors", "Surfaces",
    "Boards & Timber", "Hardware"
]

# --------------------------------------------------
# DATABASE HELPERS
# --------------------------------------------------

def save_lead(payload, table="quote_leads"):
    if not supabase:
        raise RuntimeError("Supabase is not configured.")

    supabase.table(table).insert(payload).execute()
    return True


def common():
    return {
        "whatsapp_number": WHATSAPP_NUMBER,
        "phone_display": PHONE_DISPLAY,
        "site_url": SITE_URL
    }


@app.context_processor
def inject_globals():
    return common()


def _product_view(row):
    return {
        "id": row.get("id"),
        "slug": row.get("slug", ""),
        "name": row.get("name", ""),
        "grade": row.get("grade") or "",
        "category": row.get("category", "Plywood"),
        "desc": row.get("description") or "",
        "best": row.get("best_for") or "",
        "thickness": row.get("thickness") or "",
        "warranty": row.get("warranty") or "",
        "badge": row.get("badge") or "",
        "image": row.get("image_url") or "",
        "published": bool(row.get("published", True))
    }


def get_products(include_unpublished=False):
    if supabase:
        try:
            query = (
                supabase.table("products")
                .select("*")
                .order("sort_order")
                .order("name")
            )

            if not include_unpublished:
                query = query.eq("published", True)

            rows = query.limit(500).execute().data or []
            return [_product_view(row) for row in rows]

        except Exception:
            app.logger.exception("Could not load products from Supabase.")

    return [dict(product, published=True) for product in PRODUCTS]


def get_site_content():
    if not supabase:
        return {}

    try:
        rows = (
            supabase.table("site_content")
            .select("*")
            .execute()
            .data or []
        )

        return {
            row["content_key"]: row
            for row in rows
        }

    except Exception:
        app.logger.exception("Could not load site content.")
        return {}


@app.context_processor
def inject_site_content():
    return {"site_content": get_site_content()}


# --------------------------------------------------
# PUBLIC WEBSITE ROUTES
# --------------------------------------------------

@app.get("/")
def home():
    return render_template(
        "index.html",
        products=get_products(),
        categories=CATEGORIES
    )


@app.get("/products")
def products():
    category = request.args.get("category", "")
    catalogue = get_products()

    filtered = [
        product for product in catalogue
        if not category or product["category"] == category
    ]

    return render_template(
        "products.html",
        products=filtered,
        categories=CATEGORIES,
        selected=category
    )


@app.get("/<slug>")
def product_detail(slug):
    catalogue = get_products()

    product = next(
        (item for item in catalogue if item["slug"] == slug),
        None
    )

    if not product:
        abort(404)

    return render_template(
        "product.html",
        product=product,
        products=catalogue
    )


@app.route("/ply-finder", methods=["GET", "POST"])
def ply_finder():
    recommendation = None

    if request.method == "POST":
        use = request.form.get("use", "furniture")
        moisture = request.form.get("moisture", "dry")

        catalogue = get_products()

        if use == "construction":
            target = "shuttering-plywood"
        elif moisture == "wet":
            target = "bwp-plywood"
        elif moisture == "occasional":
            target = "bwr-plywood"
        else:
            target = "mr-plywood"

        recommendation = next(
            (item for item in catalogue if item["slug"] == target),
            None
        )

    return render_template(
        "ply_finder.html",
        recommendation=recommendation
    )


@app.get("/professionals")
def professionals():
    return render_template("professionals.html")


@app.route("/become-a-dealer", methods=["GET", "POST"])
def dealer():
    if request.method == "POST":

        # These names match the dealer_applications table.
        data = {
            "contact_name": request.form.get("name", "").strip(),
            "business_name": request.form.get("business", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "city": request.form.get("city", "").strip(),
            "gst_number": request.form.get("gst", "").strip(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        if (
            not data["contact_name"]
            or not data["phone"]
            or not data["city"]
        ):
            flash(
                "Please complete your name, phone and city.",
                "error"
            )
        else:
            try:
                save_lead(data, "dealer_applications")
                return redirect(url_for("thank_you", kind="dealer"))

            except Exception:
                app.logger.exception("Dealer application save failed.")

                flash(
                    "We couldn't submit your application. Please try WhatsApp or call us.",
                    "error"
                )

    return render_template("dealer.html", cities=CITIES)


@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/cities/<city_slug>")
def city_page(city_slug):
    city = city_slug.replace("-", " ").title()

    if city not in CITIES:
        abort(404)

    return render_template("city.html", city=city)


@app.get("/resources")
def resources():
    articles = [
        (
            "BWP vs BWR vs MR plywood",
            "Understand the differences between common plywood grades and where each may be suitable."
        ),
        (
            "Choosing plywood for a kitchen",
            "What to consider when selecting panels for a high-use kitchen."
        ),
        (
            "Plywood thickness guide: 6 mm to 25 mm",
            "A practical overview of common thicknesses and typical applications."
        ),
        (
            "What is calibrated plywood?",
            "How uniform thickness can help furniture fabrication."
        ),
        (
            "Blockboard vs plywood",
            "Where blockboards and plywood differ in construction and use."
        ),
        (
            "A guide to laminates and veneers",
            "Compare decorative laminates with natural wood veneers."
        )
    ]

    return render_template("resources.html", articles=articles)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return handle_quote()

    return render_template("contact.html")


@app.post("/quote")
def quote():
    return handle_quote()


def handle_quote():
    fields = [
        "name", "phone", "customer_type", "product",
        "thickness", "quantity", "finish", "location",
        "address", "message"
    ]

    data = {
        key: request.form.get(key, "").strip()
        for key in fields
    }

    data["source_page"] = request.form.get(
        "source_page",
        "Website"
    )

    data["created_at"] = datetime.now(timezone.utc).isoformat()

    if (
        not data["name"]
        or not data["phone"]
        or not data["customer_type"]
    ):
        flash(
            "Please complete your name, WhatsApp number and customer type.",
            "error"
        )

        return redirect(request.referrer or url_for("contact"))

    try:
        save_lead(data, "quote_leads")
        return redirect(url_for("thank_you", kind="quote"))

    except Exception:
        app.logger.exception("Quote submission failed.")

        flash(
            "Your enquiry could not be saved right now. Please contact us on WhatsApp or phone.",
            "error"
        )

        return redirect(request.referrer or url_for("contact"))


@app.get("/thank-you/<kind>")
def thank_you(kind):
    if kind not in ["quote", "dealer"]:
        abort(404)

    return render_template("thank_you.html", kind=kind)


# --------------------------------------------------
# SEO AND HEALTH ROUTES
# --------------------------------------------------

@app.get("/robots.txt")
def robots():
    return (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE_URL.rstrip('/')}/sitemap.xml\n"
    ), 200, {"Content-Type": "text/plain"}


@app.get("/sitemap.xml")
def sitemap():
    urls = [
        url_for("home", _external=True),
        url_for("products", _external=True),
        url_for("ply_finder", _external=True),
        url_for("professionals", _external=True),
        url_for("dealer", _external=True),
        url_for("about", _external=True),
        url_for("resources", _external=True),
        url_for("contact", _external=True)
    ]

    urls += [
        url_for(
            "product_detail",
            slug=product["slug"],
            _external=True
        )
        for product in get_products()
    ]

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(
            f"<url><loc>{url}</loc></url>"
            for url in urls
        )
        + "</urlset>"
    )

    return make_response(
        xml,
        200,
        {"Content-Type": "application/xml"}
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "supabase_configured": bool(supabase)
    }


# --------------------------------------------------
# ADMIN SECURITY
# --------------------------------------------------

def admin_csrf_token():
    token = session.get("admin_csrf")

    if not token:
        token = secrets.token_urlsafe(32)
        session["admin_csrf"] = token

    return token


@app.context_processor
def inject_admin_csrf():
    return {"admin_csrf_token": admin_csrf_token}


def verify_admin_csrf():
    submitted = request.form.get("csrf_token", "")
    expected = session.get("admin_csrf", "")

    if (
        not submitted
        or not expected
        or not hmac.compare_digest(submitted, expected)
    ):
        abort(
            400,
            description="Invalid form security token. Refresh and try again."
        )


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(
                url_for("admin_login", next=request.path)
            )

        return view(*args, **kwargs)

    return wrapped


def admin_table_rows(table, limit=200):
    if not supabase:
        raise RuntimeError("Supabase is not configured.")

    return (
        supabase.table(table)
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
        .data or []
    )


# --------------------------------------------------
# ADMIN LOGIN AND LOGOUT
# --------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if session.get("is_admin"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        verify_admin_csrf()

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        valid_user = (
            bool(ADMIN_USERNAME)
            and hmac.compare_digest(username, ADMIN_USERNAME)
        )

        valid_password = (
            bool(ADMIN_PASSWORD_HASH)
            and check_password_hash(ADMIN_PASSWORD_HASH, password)
        )

        if valid_user and valid_password:
            session.clear()

            session["is_admin"] = True
            session["admin_username"] = username
            session.permanent = True

            admin_csrf_token()

            return redirect(url_for("admin_dashboard"))

        flash("Incorrect admin username or password.", "error")

    return render_template("admin/login.html")


@app.post("/admin/logout")
@admin_required
def admin_logout():
    verify_admin_csrf()

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("admin_login"))


# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------

@app.get("/admin")
@app.get("/admin/dashboard")
@admin_required
def admin_dashboard():

    if not supabase:
        flash(
            "Supabase is not configured. Check your environment variables.",
            "error"
        )

        return render_template(
            "admin/dashboard.html",
            leads=[],
            dealers=[],
            lead_count=0,
            dealer_count=0,
            new_count=0,
            products_count=0
        )

    try:
        leads = admin_table_rows("quote_leads", 8)
        dealers = admin_table_rows("dealer_applications", 8)

        all_leads = (
            supabase.table("quote_leads")
            .select("id,status")
            .limit(1000)
            .execute()
            .data or []
        )

        all_dealers = (
            supabase.table("dealer_applications")
            .select("id,status")
            .limit(1000)
            .execute()
            .data or []
        )

        products_count = len(
            supabase.table("products")
            .select("id")
            .limit(1000)
            .execute()
            .data or []
        )

        new_count = sum(
            1
            for item in all_leads + all_dealers
            if item.get("status", "New") == "New"
        )

        return render_template(
            "admin/dashboard.html",
            leads=leads,
            dealers=dealers,
            lead_count=len(all_leads),
            dealer_count=len(all_dealers),
            new_count=new_count,
            products_count=products_count
        )

    except Exception:
        app.logger.exception("Admin dashboard could not load data.")

        flash(
            "Could not load records. Check that the SQL migration has been run.",
            "error"
        )

        return render_template(
            "admin/dashboard.html",
            leads=[],
            dealers=[],
            lead_count=0,
            dealer_count=0,
            new_count=0,
            products_count=0
        )


# --------------------------------------------------
# ADMIN ENQUIRIES AND DEALER APPLICATIONS
# --------------------------------------------------

@app.get("/admin/enquiries")
@admin_required
def admin_enquiries():

    try:
        rows = admin_table_rows("quote_leads", 500)

    except Exception:
        app.logger.exception("Could not load enquiries.")
        rows = []

        flash(
            "Could not load enquiries. Check the Supabase setup.",
            "error"
        )

    return render_template(
        "admin/records.html",
        rows=rows,
        record_type="enquiries",
        title="Customer enquiries"
    )


@app.get("/admin/dealers")
@admin_required
def admin_dealers():

    try:
        rows = admin_table_rows("dealer_applications", 500)

    except Exception:
        app.logger.exception("Could not load dealer applications.")
        rows = []

        flash(
            "Could not load dealer applications. Check the Supabase setup.",
            "error"
        )

    return render_template(
        "admin/records.html",
        rows=rows,
        record_type="dealers",
        title="Dealer applications"
    )


@app.post("/admin/status/<record_type>/<record_id>")
@admin_required
def admin_update_status(record_type, record_id):

    verify_admin_csrf()

    table = {
        "enquiries": "quote_leads",
        "dealers": "dealer_applications"
    }.get(record_type)

    status = request.form.get("status", "")

    allowed = {
        "New",
        "Contacted",
        "In Progress",
        "Completed",
        "Rejected"
    }

    if not table or status not in allowed:
        abort(400)

    try:
        supabase.table(table).update(
            {"status": status}
        ).eq("id", record_id).execute()

        flash("Record status updated.", "success")

    except Exception:
        app.logger.exception("Status update failed.")

        flash(
            "Status could not be updated. Check the SQL migration.",
            "error"
        )

    destination = (
        "admin_enquiries"
        if record_type == "enquiries"
        else "admin_dealers"
    )

    return redirect(url_for(destination))


@app.get("/admin/export/<record_type>.csv")
@admin_required
def admin_export(record_type):

    table = {
        "enquiries": "quote_leads",
        "dealers": "dealer_applications"
    }.get(record_type)

    if not table:
        abort(404)

    try:
        rows = admin_table_rows(table, 5000)

        output = io.StringIO()

        fields = sorted({
            key
            for row in rows
            for key in row.keys()
        })

        writer = csv.DictWriter(
            output,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(rows)

        response = make_response(
            "\ufeff" + output.getvalue()
        )

        response.headers["Content-Type"] = "text/csv; charset=utf-8"

        response.headers["Content-Disposition"] = (
            f"attachment; filename=kohinoor-{record_type}.csv"
        )

        return response

    except Exception:
        app.logger.exception("CSV export failed.")

        flash(
            "Export failed. Please check the Supabase connection.",
            "error"
        )

        return redirect(url_for("admin_dashboard"))


# --------------------------------------------------
# FULL WEBSITE MANAGEMENT: PRODUCTS
# --------------------------------------------------

def _slugify(value):
    import re

    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")

    return value[:90]


def _product_payload(form):

    name = form.get("name", "").strip()
    slug = _slugify(form.get("slug") or name)
    category = form.get("category", "").strip()

    if not name or not slug or not category:
        raise ValueError(
            "Product name, slug and category are required."
        )

    return {
        "name": name,
        "slug": slug,
        "category": category,
        "grade": form.get("grade", "").strip(),
        "description": form.get("description", "").strip(),
        "best_for": form.get("best_for", "").strip(),
        "thickness": form.get("thickness", "").strip(),
        "warranty": form.get("warranty", "").strip(),
        "badge": form.get("badge", "").strip(),
        "image_url": form.get("image_url", "").strip(),
        "published": form.get("published") == "on",
        "updated_at": datetime.now(timezone.utc).isoformat()
    }


@app.get("/admin/products")
@admin_required
def admin_products():

    try:
        rows = (
            supabase.table("products")
            .select("*")
            .order("sort_order")
            .order("name")
            .limit(500)
            .execute()
            .data or []
        )

    except Exception:
        app.logger.exception("Could not load products.")
        rows = []

        flash(
            "Could not load products. Run the latest SQL migration first.",
            "error"
        )

    return render_template(
        "admin/products.html",
        rows=rows
    )


@app.route("/admin/products/new", methods=["GET", "POST"])
@admin_required
def admin_product_new():

    if request.method == "POST":
        verify_admin_csrf()

        try:
            payload = _product_payload(request.form)

            supabase.table("products").insert(
                payload
            ).execute()

            flash("Product created.", "success")

            return redirect(url_for("admin_products"))

        except ValueError as exc:
            flash(str(exc), "error")

        except Exception:
            app.logger.exception("Product creation failed.")

            flash(
                "Product could not be created. Check for a duplicate slug and verify the migration.",
                "error"
            )

    return render_template(
        "admin/product_form.html",
        product={},
        page_title="Add product"
    )


@app.route("/admin/products/<product_id>/edit", methods=["GET", "POST"])
@admin_required
def admin_product_edit(product_id):

    try:
        result = (
            supabase.table("products")
            .select("*")
            .eq("id", product_id)
            .limit(1)
            .execute()
            .data or []
        )

        if not result:
            abort(404)

        product = result[0]

    except Exception:
        app.logger.exception("Product could not be loaded.")
        abort(404)

    if request.method == "POST":
        verify_admin_csrf()

        try:
            payload = _product_payload(request.form)

            supabase.table("products").update(
                payload
            ).eq("id", product_id).execute()

            flash("Product updated.", "success")

            return redirect(url_for("admin_products"))

        except ValueError as exc:
            flash(str(exc), "error")

        except Exception:
            app.logger.exception("Product update failed.")

            flash(
                "Product could not be updated. Check that the slug is unique.",
                "error"
            )

    return render_template(
        "admin/product_form.html",
        product=product,
        page_title="Edit product"
    )


@app.post("/admin/products/<product_id>/delete")
@admin_required
def admin_product_delete(product_id):

    verify_admin_csrf()

    try:
        supabase.table("products").delete().eq(
            "id", product_id
        ).execute()

        flash("Product deleted.", "success")

    except Exception:
        app.logger.exception("Product delete failed.")
        flash("Product could not be deleted.", "error")

    return redirect(url_for("admin_products"))


# --------------------------------------------------
# FULL WEBSITE MANAGEMENT: CONTENT
# --------------------------------------------------

@app.route("/admin/content", methods=["GET", "POST"])
@admin_required
def admin_content():

    if request.method == "POST":
        verify_admin_csrf()

        allowed_keys = [
            "home_hero",
            "home_intro",
            "about_intro",
            "footer_text"
        ]

        try:
            for key in allowed_keys:

                title = request.form.get(
                    f"{key}_title", ""
                ).strip()

                body = request.form.get(
                    f"{key}_body", ""
                ).strip()

                payload = {
                    "content_key": key,
                    "title": title,
                    "body": body,
                    "updated_at": datetime.now(
                        timezone.utc
                    ).isoformat()
                }

                existing = (
                    supabase.table("site_content")
                    .select("id")
                    .eq("content_key", key)
                    .limit(1)
                    .execute()
                    .data or []
                )

                if existing:
                    (
                        supabase.table("site_content")
                        .update(payload)
                        .eq("content_key", key)
                        .execute()
                    )
                else:
                    (
                        supabase.table("site_content")
                        .insert(payload)
                        .execute()
                    )

            flash("Website content saved.", "success")

            return redirect(url_for("admin_content"))

        except Exception:
            app.logger.exception("Website content save failed.")

            flash(
                "Content could not be saved. Run the latest SQL migration.",
                "error"
            )

    return render_template(
        "admin/content.html",
        content=get_site_content()
    )


# --------------------------------------------------
# SECURITY HEADERS
# --------------------------------------------------

@app.after_request
def add_security_headers(response):

    response.headers.setdefault(
        "X-Content-Type-Options",
        "nosniff"
    )

    response.headers.setdefault(
        "X-Frame-Options",
        "DENY"
    )

    response.headers.setdefault(
        "Referrer-Policy",
        "strict-origin-when-cross-origin"
    )

    return response


# --------------------------------------------------
# LOCAL DEVELOPMENT
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG") == "1"
    )