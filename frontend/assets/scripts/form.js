
// =======================
// ADD MORE PRODUCT
// =======================

function add_more_product() {
    const products_container = document.getElementById("products-container");

    // clone first product
    const product1 = products_container.querySelector(".product-item");
    const clone = product1.cloneNode(true);     // (true) -> deep cloning -> clones all child nodes as well, not just the outer element itself

    // get new product number
    const product_count = products_container.children.length + 1;

    // update product heading
    const heading = clone.querySelector(".product-title");
    if (heading) {
        initial_heading = heading.textContent.replace(/\d+/g, "");
        heading.textContent = initial_heading + product_count;
    }

    // clear values inside clone of first product's fields
    clone.querySelectorAll("input, textarea").forEach(el => {
        el.value = "";
    });

    // append new product
    products_container.appendChild(clone);
}


// =======================
// ENABLE INPUT BOX (EDIT BUTTON)
// =======================

function enable_input_box(ele_id) {

    console.log({ele_id});

    // get ele by id
    const input_field = document.getElementById(ele_id);

    // enable it
    input_field.readOnly = false;
}


// =======================
// THEME SWITCHING
// =======================

function set_theme(theme) {

    console.log({theme});

    // update bootstrap theme in body tag
    document.body.setAttribute("data-bs-theme", theme);

    // update theme CSS file (if using separate files)
    const themeLink = document.querySelector('link[href*="themes"]');

    if (themeLink) {
        themeLink.href = `/assets/stylesheets/themes/${theme}.css`;
    }

    // store theme in local storage (so it persists on reload)
    localStorage.setItem("theme", theme);
}

// =======================
// LOAD SAVED THEME
// =======================

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme) {
        set_theme(savedTheme);
    }
});


// =====================================================================
// SUBMIT ALL FORMS
// =====================================================================

function get_fields_data(fields) {
    const fields_json = {};

    fields.forEach(field => {
        let key = field.id || field.name;

        // skip if no identifier
        if (!key) return;

        // RADIO BUTTON
        if (field.type === "radio") {
            if (field.checked) {
                fields_json[field.name] = field.value;
            }
        }

        // NORMAL INPUTS
        else {
            fields_json[key] = field.value;
        }
    });

    return fields_json;
}

function get_form_data(form, formId) {
    // 🔥 SPECIAL HANDLING FOR PRODUCTS FORM
    if (formId === "products_form") {
        const products_data = [];

        const all_product_items = form.querySelectorAll(".product-item")    // fetching all products

        all_product_items.forEach((item, index) => {

            product_item_fields = item.querySelectorAll("input, textarea, select"); // fetching product's all fields

            product_item_fields_dict = get_fields_data(product_item_fields);

            products_data.push(product_item_fields_dict);
        });

        return products_data;
    }

    // 🔥 ALL OTHER FORMS
    // get all inputs inside form
    const form_fields = form.querySelectorAll("input, textarea, select");

    form_fields_dict = get_fields_data(form_fields);

    return form_fields_dict;
}

function get_all_forms_data() {
    const all_forms_data = {};

    const all_forms = document.querySelectorAll("form");

    all_forms.forEach(form => {
        form_id = form.id;
        form_action = form.getAttribute("action");

        // console.log({form_id, form_action});

        form_data = get_form_data(form, form_id);

        all_forms_data[form_id] = {
            id: form_id,
            action: form_action,
            data: form_data
        };

    });
    // console.log("=== ALL FORM DATA ===");
    // console.log({all_forms_data});

    return all_forms_data;
}

const callApi = (api, method, data) => fetch(api, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});

async function submit_all_forms() {
    // GET ALL FORMS DATA
    const all_forms_data = get_all_forms_data();

    const results = [];

    // for (const form in all_forms_data) {
    Object.entries(all_forms_data).forEach(async ([k, v]) => {
        // 🚀 CALL API
        try {
            console.log(`Calling ${v.id} API: ${v.action} with data:`, v.data);
            const response = await callApi(
                api=v.action,
                method='POST',
                data=v.data
            );
            const result = await response.json();

            results.push({
                formId: v.id,
                status: response.status,
                response: result
            });

        } catch (error) {
            results.push({
                formId: v.id,
                error: error.message
            });
        }
    });

    // console.log("=== API RESULTS ===");
    // console.log(results);

}



