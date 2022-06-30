@app.route('/product/<product_id>')
def product(product_id):
    opinions = pd.read_json(f"app/opinions/{product_id}.json")
    stats={
        "opinions_count": len(opinions),
        "pros_count": opinions["pros"].map(bool).sum(),
        "cons_count": opinions["cons"].map(bool).sum(),
        "average_score": opinions["score"].mean().round(2)
    }
    if not os.path.exists("app/static/plots"):
        os.makedirs("app/static/plots")
    recommendations = opinions["rcmd"].value_counts(
        dropna=False).sort_index().reindex([False, True, None])
    recommendations.plot.pie(
        label = "",
        title = "Recommendations: "+product_id,
        labels = ["Not recommend", "Recommend", "No opinion"],
        colors = ["crimson", "forestgreen", "grey"],
        autopct = lambda p: f"{p:.1f}%" if p>0 else ""
    )
    plt.savefig(f"app/static/plots/{product_id}_rcmd.png")
    plt.close()
    stars = opinions["score"].value_counts(
        dropna=False).sort_index().reindex(np.arange(0,5.5,0.5))
    stars.plot.bar(
        label = "",
        title = "Stars score: "+product_id,
        xlabel = "Stars values",
        ylabel = "Opinions count",
        color = "hotpink",
        rot = 0
    )
    plt.savefig(f"app/static/plots/{product_id}_stars.png")
    plt.close()
    return render_template("product.html.jinja", product_id=product_id, stats=stats, opinions=opinions)