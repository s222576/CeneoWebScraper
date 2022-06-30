@app.route('/opinions', methods=["POST"])
def opinions():
    product_id = request.form.get("product_id")
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    all_opinions = []
    while (url):
        print(url)
        response = requests.get(url)
        page_dom = BeautifulSoup(response.text, "html.parser")
        opinions = page_dom.select("div.js_product-review")
        for opinion in opinions:
            single_opinion = {
                key: get_element(opinion, *values)
                for key, values in opinion_elements.items() 
            }
            single_opinion["opinion_id"] = opinion["data-entry-id"]
            single_opinion["rcmd"] = True if single_opinion["rcmd"] == "Polecam" else False if single_opinion["rcmd"] == "Nie polecam" else None
            single_opinion["score"] = float(single_opinion["score"].split("/")[0].replace(",", "."))
            single_opinion["useful_for"] = int(single_opinion["useful_for"])
            single_opinion["useless_for"] = int(single_opinion["useless_for"])
            single_opinion["content_en"] = translate(single_opinion["content"]) if single_opinion["content"] else ""
            single_opinion['pros_en'] = translate(single_opinion['pros']) if single_opinion["pros"] else ""
            single_opinion['cons_en'] = translate(single_opinion['cons']) if single_opinion["cons"] else ""
            all_opinions.append(single_opinion)
        try:
            url = "https://www.ceneo.pl"+get_element(page_dom,"a.pagination__next","href")
        except TypeError: 
            url = None
    if not os.path.exists("app/opinions"):
        os.makedirs("app/opinions")
    with open(f"app/opinions/{product_id}.json", "w", encoding="UTF-8") as jf:
        json.dump(all_opinions, jf, indent=4, ensure_ascii=False)
    return redirect(url_for("product", product_id=product_id))