import os, re, json
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, abort, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-before-deployment")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as exc:
        app.logger.warning("Supabase client could not initialise: %s", exc)

BUSINESS = {
    "name": os.getenv("BUSINESS_NAME", "Kohinoor Timber Traders"),
    "phone": os.getenv("BUSINESS_PHONE", "+91XXXXXXXXXX"),
    "whatsapp": re.sub(r"\D", "", os.getenv("WHATSAPP_NUMBER", "91XXXXXXXXXX")),
    "email": os.getenv("BUSINESS_EMAIL", "enquiries@example.com"),
    "address": os.getenv("BUSINESS_ADDRESS", "Mumbai, Maharashtra, India"),
    "hours": os.getenv("BUSINESS_HOURS", "Monday – Saturday, 10:00 AM – 7:00 PM"),
}

PRODUCTS = [
 {"slug":"bwp-plywood","name":"Kohinoor Gold BWP Plywood","short":"Built for demanding spaces and long-term performance.","grade":"BWP","tier":"Kohinoor Gold","thickness":"6, 8, 12, 16, 19 and 25 mm","best_for":"Kitchens, utility areas and demanding interior applications","description":"A premium boiling-water-proof plywood option for projects where dependable bonding and strength matter.","features":["Hardwood (gurjan) core, as stated in the project brief","Phenolic resin bonding","Preservative treatment against termites and borers","Available thickness range from 6–25 mm"],"warranty":"Up to 21 years, subject to certificate verification"},
 {"slug":"bwr-plywood","name":"Kohinoor Premium BWR Plywood","short":"A considered choice for areas exposed to occasional moisture.","grade":"BWR","tier":"Kohinoor Premium","thickness":"6, 8, 12, 16, 19 and 25 mm","best_for":"Kitchens, furniture and interior applications","description":"A boiling-water-resistant grade for projects that need a balance of dependable performance and value.","features":["Moisture-resistant bonding specification","Multiple thickness options","Suitable for a range of furniture applications"],"warranty":"7–15 years across applicable grades; confirm product-specific terms"},
 {"slug":"mr-plywood","name":"Kohinoor Classic MR Plywood","short":"A practical choice for everyday dry interior applications.","grade":"MR","tier":"Kohinoor Classic","thickness":"6, 8, 12, 16, 19 and 25 mm","best_for":"Bedroom furniture, shelves and dry interior spaces","description":"A moisture-resistant plywood option for everyday interior furniture and joinery.","features":["For dry interior applications","Multiple thickness options","Suitable for furniture and cabinetry"],"warranty":"Confirm applicable product warranty"},
 {"slug":"calibrated-plywood","name":"Calibrated Plywood","short":"Uniform thickness for a cleaner, more precise finish.","grade":"Calibrated","tier":"Kohinoor range","thickness":"Available sizes: confirm current stock","best_for":"Modular furniture, wardrobes and precision joinery","description":"Calibrated panels help support consistent dimensions and a flatter finish in furniture work.","features":["Uniform thickness","Flat, clean finish","Useful for precision furniture work"],"warranty":"Confirm product-specific terms"},
 {"slug":"marine-plywood","name":"Marine Plywood","short":"For applications that call for a specialised plywood specification.","grade":"Marine","tier":"Kohinoor range","thickness":"Available sizes: confirm current stock","best_for":"Specified marine and high-moisture applications","description":"Ask our team to confirm the appropriate marine specification and intended use before ordering.","features":["Discuss application and specification with our team","Thickness options subject to availability","Project quantity enquiries welcome"],"warranty":"Confirm after specification and certificate review"},
 {"slug":"flexible-plywood","name":"Flexible Plywood","short":"A useful panel option for curved furniture and design details.","grade":"Flexible","tier":"Kohinoor range","thickness":"Confirm current stock","best_for":"Curved surfaces, rounded counters and feature furniture","description":"Flexible plywood is used where a design calls for shaped or curved panel work.","features":["For curved design applications","Discuss bend radius and installation with your fabricator","Availability on request"],"warranty":"Confirm product-specific terms"},
 {"slug":"shuttering-plywood","name":"Kohinoor Shield Shuttering Plywood","short":"A site-focused panel for formwork requirements.","grade":"Film-faced / Shuttering","tier":"Kohinoor Shield","thickness":"Confirm current stock","best_for":"Construction formwork and concrete shuttering","description":"A shuttering panel option for contractors and construction projects. Confirm reuse expectations and site conditions with the supplier.","features":["Film-faced shuttering range","Bulk and project enquiries welcome","Confirm panel specification before purchase"],"warranty":"Confirm product-specific terms"},
 {"slug":"blockboards-doors","name":"Block Boards & Flush Doors","short":"Panels and door solutions for interior projects.","grade":"Block board / Flush door","tier":"Kohinoor range","thickness":"Block boards in 19 and 25 mm; door options on request","best_for":"Doors, partitions and furniture","description":"Block boards and flush doors, including teak-veneer options, for residential and commercial projects.","features":["19 mm and 25 mm block boards","Flush doors including teak veneer options","Project supply enquiries welcome"],"warranty":"Confirm product-specific terms"},
 {"slug":"laminates-veneers","name":"Laminates & Veneers","short":"Finishes that bring character to furniture and interiors.","grade":"Decorative surfaces","tier":"Kohinoor collection","thickness":"Laminates in 0.8, 1.0 and 1.25 mm","best_for":"Cabinet fronts, wardrobes, counters and furniture","description":"A collection of laminate and veneer options, including standard and exotic veneers.","features":["0.8, 1.0 and 1.25 mm laminate options","Standard and exotic veneers","Finish selection assistance"],"warranty":"As per the selected manufacturer's terms"},
 {"slug":"timber-mdf-boards","name":"Timber, MDF & Boards","short":"A broad material range for trade and project requirements.","grade":"Timber and engineered boards","tier":"Kohinoor Timber Traders","thickness":"Confirm stock and dimensions","best_for":"Furniture, joinery, fit-outs and project supply","description":"Teak, sal and pine timber, MDF, HDHMR and particle board options.","features":["Teak, sal and pine timber","MDF and HDHMR for interior/exterior applications","Particle board options"],"warranty":"Depends on selected material and manufacturer"},
 {"slug":"hardware","name":"Hardware & Accessories","short":"The practical details that complete an installation.","grade":"Hardware","tier":"Kohinoor Timber Traders","thickness":"Multiple options","best_for":"Cabinetry, doors and furniture installations","description":"Adhesives, hinges, channels, locks and handles for furniture and interior work.","features":["Adhesives","Hinges and channels","Locks and handles"],"warranty":"As per the selected manufacturer's terms"},
]
PRODUCT_MAP = {p["slug"]: p for p in PRODUCTS}
CITIES = ["Mumbai", "Thane", "Navi Mumbai", "Kalyan", "Vasai-Virar", "Pune", "Nashik", "Nagpur", "Aurangabad"]
BLOGS = [
 ("bwp-vs-bwr-vs-mr","BWP vs BWR vs MR Plywood: Understanding the Difference","A practical guide to grades, moisture exposure and choosing the right specification."),
 ("best-plywood-for-kitchen","Which Plywood Is Suitable for a Kitchen?","Understand the role of moisture, installation and grade selection in kitchen projects."),
 ("plywood-thickness-guide","Plywood Thickness Guide: 6 mm to 25 mm","Where different thicknesses are commonly considered in furniture and interiors."),
 ("calibrated-plywood-guide","What Is Calibrated Plywood?","Why uniform thickness can matter for modular furniture and clean finishes."),
 ("blockboard-vs-plywood","Block Board vs Plywood: Where Each Fits","A straightforward comparison for doors, partitions and furniture."),
 ("questions-before-buying","Questions to Ask Before Buying Plywood","A checklist for homeowners, carpenters, architects and contractors.")
]

def save_record(table, payload):
    if not supabase:
        app.logger.info("Supabase not configured; lead not persisted. Payload keys: %s", list(payload))
        return False
    try:
        supabase.table(table).insert(payload).execute()
        return True
    except Exception as exc:
        app.logger.exception("Supabase insert failed: %s", exc)
        return False

@app.context_processor
def inject_globals():
    return {"business": BUSINESS, "products": PRODUCTS, "cities": CITIES, "blogs": BLOGS}

@app.get("/")
def home():
    return render_template("home.html", title="Kohinoor Plywood | Built on Trust. Crafted to Last.")

@app.get("/products")
def product_listing():
    return render_template("products.html", title="Plywood, Boards, Doors & More | Kohinoor")

@app.get("/plywood/<slug>")
def product_detail(slug):
    product = PRODUCT_MAP.get(slug)
    if not product: abort(404)
    return render_template("product.html", product=product, title=f'{product["name"]} | Kohinoor Plywood')

@app.get("/ply-finder")
def ply_finder():
    return render_template("finder.html", title="Ply Finder | Find a Suitable Grade")

@app.get("/professionals")
def professionals():
    return render_template("professionals.html", title="For Architects, Designers & Contractors")

@app.get("/become-a-dealer")
def dealer():
    return render_template("dealer.html", title="Become a Kohinoor Plywood Dealer")

@app.get("/dealer-thank-you")
def dealer_thanks():
    return render_template("thank_you.html", title="Dealer application received", kind="dealer")

@app.get("/about")
def about():
    return render_template("about.html", title="Our Story & Quality | Kohinoor")

@app.get("/cities/<city_slug>")
def city_page(city_slug):
    city = city_slug.replace("-", " ").title()
    if city not in CITIES: abort(404)
    return render_template("city.html", city=city, title=f"Plywood Supplier in {city} | Kohinoor")

@app.get("/resources")
def resources():
    return render_template("resources.html", title="Plywood Buying Guides | Kohinoor")

@app.get("/resources/<slug>")
def resource_detail(slug):
    blog = next((b for b in BLOGS if b[0] == slug), None)
    if not blog: abort(404)
    return render_template("resource_detail.html", blog=blog, title=blog[1])

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return handle_quote()
    return render_template("contact.html", title="Contact & Get a Quote | Kohinoor")

@app.post("/quote")
def quote():
    return handle_quote()

def handle_quote():
    data = {
      "name": request.form.get("name","").strip(),
      "phone": request.form.get("phone","").strip(),
      "customer_type": request.form.get("customer_type","").strip(),
      "product": request.form.get("product","").strip(),
      "thickness": request.form.get("thickness","").strip(),
      "quantity": request.form.get("quantity","").strip(),
      "finish": request.form.get("finish","").strip(),
      "delivery_location": request.form.get("delivery_location","").strip(),
      "address": request.form.get("address","").strip(),
      "source_page": request.form.get("source_page","Website"),
      "created_at": datetime.now(timezone.utc).isoformat()
    }
    if len(data["name"]) < 2 or not re.fullmatch(r"[6-9]\d{9}", re.sub(r"\D","",data["phone"])):
        flash("Please enter your name and a valid 10-digit Indian mobile number.", "error")
        return redirect(request.referrer or url_for("contact"))
    if not data["customer_type"] or not data["product"] or not data["delivery_location"]:
        flash("Please complete the required enquiry details.", "error")
        return redirect(request.referrer or url_for("contact"))
    saved = save_record("quote_leads", data)
    flash("Thank you. Your enquiry has been received." if saved else "Your enquiry is ready, but online storage is not configured. Please contact us directly.", "success" if saved else "error")
    return redirect(url_for("quote_thanks"))

@app.get("/thank-you")
def quote_thanks():
    return render_template("thank_you.html", title="Thank you", kind="quote")

@app.post("/dealer-application")
def dealer_application():
    data = {k: request.form.get(k,"").strip() for k in ["contact_name","business_name","phone","email","city","gst_number","current_brands","monthly_volume"]}
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    if not data["contact_name"] or not data["business_name"] or not re.fullmatch(r"[6-9]\d{9}", re.sub(r"\D","",data["phone"])):
        flash("Please provide a contact name, business name and valid 10-digit mobile number.", "error")
        return redirect(url_for("dealer"))
    saved = save_record("dealer_applications", data)
    flash("Application received." if saved else "Application form validated, but database storage is not configured.", "success" if saved else "error")
    return redirect(url_for("dealer_thanks"))

@app.post("/api/events")
def track_event():
    payload = request.get_json(silent=True) or {}
    event_name = str(payload.get("event_name",""))[:80]
    if event_name not in {"quote_click","whatsapp_click","call_click","catalogue_download","quote_submit","dealer_submit","ply_finder_complete"}:
        return jsonify({"ok":False}), 400
    save_record("site_events", {"event_name":event_name, "page":str(payload.get("page",""))[:200], "created_at":datetime.now(timezone.utc).isoformat()})
    return jsonify({"ok":True})

@app.get("/robots.txt")
def robots():
    return app.response_class("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n", mimetype="text/plain")

@app.get("/sitemap.xml")
def sitemap():
    urls = [url_for("home",_external=True),url_for("product_listing",_external=True),url_for("ply_finder",_external=True),url_for("professionals",_external=True),url_for("dealer",_external=True),url_for("about",_external=True),url_for("resources",_external=True),url_for("contact",_external=True)]
    urls += [url_for("product_detail",slug=p["slug"],_external=True) for p in PRODUCTS]
    urls += [url_for("city_page",city_slug=c.lower().replace(" ","-"),_external=True) for c in CITIES]
    xml = '<?xml version="1.0" encoding="UTF-8"?>' + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>"
    return app.response_class(xml, mimetype="application/xml")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", title="Page not found"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
