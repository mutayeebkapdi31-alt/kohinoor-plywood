document.addEventListener("DOMContentLoaded", () => {
  const menu = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  if (menu && nav) menu.addEventListener("click", () => {
    const open = menu.getAttribute("aria-expanded") === "true";
    menu.setAttribute("aria-expanded", String(!open));
    nav.classList.toggle("is-open", !open);
    document.body.classList.toggle("menu-open", !open);
  });

  // Track conversion actions. The server stores only approved event names.
  document.querySelectorAll("[data-track]").forEach(el => {
    el.addEventListener("click", () => {
      fetch("/api/events", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({event_name:el.dataset.track, page:location.pathname})}).catch(()=>{});
    });
  });

  // Two-step quote forms: first three fields, then full requirements.
  document.querySelectorAll(".multi-step-form").forEach(form => {
    const steps = [...form.querySelectorAll(".form-step")];
    let current = 0;
    const bar = form.querySelector(".form-progress i");
    const label = form.querySelector(".step-count");
    const show = n => {
      current = n;
      steps.forEach((s,i)=>s.classList.toggle("active",i===n));
      if (bar) bar.style.width = n === 0 ? "50%" : "100%";
      if (label) label.textContent = `STEP 0${n+1} / 02`;
    };
    form.querySelector(".next-step")?.addEventListener("click", () => {
      const required = [...steps[0].querySelectorAll("[required]")];
      const valid = required.every(input => input.reportValidity());
      if (valid) show(1);
    });
    form.querySelector(".prev-step")?.addEventListener("click",()=>show(0));
    form.addEventListener("submit", e => {
      const required = [...steps[1].querySelectorAll("[required]")];
      if (!required.every(input => input.reportValidity())) { e.preventDefault(); show(1); }
    });
  });

  // Product search
  const search = document.getElementById("productSearch");
  if (search) search.addEventListener("input", () => {
    const q = search.value.toLowerCase().trim();
    let visible = 0;
    document.querySelectorAll(".catalog-card").forEach(card => {
      const show = card.dataset.search.includes(q);
      card.hidden = !show; if (show) visible++;
    });
    const empty = document.getElementById("noProducts");
    if (empty) empty.hidden = visible !== 0;
  });

  // Ply Finder quiz
  const finder = document.getElementById("plyFinder");
  if (finder) {
    const questions = [...finder.querySelectorAll(".finder-question")];
    const answers = [];
    let index = 0;
    const result = finder.querySelector("#finderResult");
    const back = finder.querySelector("#finderBack");
    const progress = finder.querySelector("#finderProgress");
    const label = finder.querySelector("#finderStepLabel");
    const count = finder.querySelector("#finderCount");
    const render = () => {
      questions.forEach((q,i)=>q.classList.toggle("active",i===index));
      back.disabled = index===0;
      progress.style.width = `${(index+1)*25}%`;
      label.textContent = `QUESTION 0${index+1} / 04`;
      count.textContent = `${index+1} of 4`;
    };
    const finish = () => {
      const [use, moisture, budget, thickness] = answers;
      let slug = "mr-plywood", title = "Kohinoor Classic MR Plywood";
      let text = "For mostly dry interior applications, MR may be a starting point to discuss with your fabricator.";
      if (use === "construction") {slug="shuttering-plywood";title="Kohinoor Shield Shuttering Plywood";text="For a construction/formwork requirement, discuss the shuttering range and site specification with our team.";}
      else if (use === "curved") {slug="flexible-plywood";title="Flexible Plywood";text="For curved furniture and shaped surfaces, ask about the flexible plywood range and suitable bending details.";}
      else if (moisture === "high" || (use === "kitchen" && budget === "premium")) {slug="bwp-plywood";title="Kohinoor Gold BWP Plywood";text="BWP is a starting point to discuss for demanding or moisture-exposed applications. Confirm the precise application and specification before selection.";}
      else if (moisture === "some" || budget === "balanced") {slug="bwr-plywood";title="Kohinoor Premium BWR Plywood";text="BWR may be worth discussing for occasional moisture exposure. Confirm suitability for the exact site conditions.";}
      const q = new URLSearchParams({product:slug, thickness:thickness==="unsure"?"":`${thickness} mm`});
      finder.querySelector("#resultTitle").textContent = title;
      finder.querySelector("#resultText").textContent = `${text} ${thickness!=="unsure"?`You selected ${thickness} mm; confirm this thickness with your designer or fabricator.`:"Our team can help discuss thickness."}`;
      finder.querySelector("#resultQuote").href = `/contact?${q.toString()}`;
      questions.forEach(q=>q.classList.remove("active"));
      result.hidden = false;
      finder.querySelector(".finder-controls").hidden = true;
      fetch("/api/events",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event_name:"ply_finder_complete",page:location.pathname})}).catch(()=>{});
    };
    questions.forEach((q,i)=>q.querySelectorAll("button").forEach(btn=>btn.addEventListener("click",()=>{
      answers[i]=btn.dataset.value;
      if (i < 3) {index++;render();} else finish();
    })));
    back.addEventListener("click",()=>{if(index>0){index--;render();}});
    const reset=()=>{answers.length=0;index=0;result.hidden=true;finder.querySelector(".finder-controls").hidden=false;render();};
    finder.querySelector("#finderReset").addEventListener("click",reset);
    finder.querySelector("#resultAgain").addEventListener("click",reset);
    render();
  }

  // Honour URL product parameter on quote page.
  const params = new URLSearchParams(location.search);
  const productParam = params.get("product");
  if (productParam) {
    const select = document.querySelector('select[name="product"]');
    if (select) {
      const option = [...select.options].find(o=>o.text.toLowerCase().includes(productParam.replaceAll("-"," "))) ||
        [...select.options].find(o=>o.text.toLowerCase().includes(productParam.split("-")[0]));
      if (option) select.value = option.value;
    }
    const thickness = params.get("thickness");
    const t = document.querySelector('select[name="thickness"]');
    if (t && thickness) t.value = thickness;
  }
});
