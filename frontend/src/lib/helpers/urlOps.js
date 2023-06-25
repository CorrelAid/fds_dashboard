export function set_url_params(selection, category) {
    let url_params;
    if (selection != null) {
        const tr = {
            jurisdictions: "jurisdiction_id",
            public_bodies: "public_body_id",
            campaigns: "campaign_id",
        };
        url_params = `?category=${tr[category]}&selection=${selection}`;
    } else {
        url_params = "";
    }
    return url_params
}