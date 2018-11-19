item_key_list = ["create_at", "goods_id", "goods_name", "goods_desc", "goods_thumbnail_url", "goods_image_url",
                 "goods_gallery_urls", "sold_quantity", "min_group_price", "min_normal_price", "mall_name",
                 "merchant_type",
                 "category_id", "category_name", "opt_id", "opt_name", "opt_ids", "cat_ids", "mall_cps", "has_coupon",
                 "coupon_min_order_amount", "coupon_discount", "coupon_total_quantity", "coupon_remain_quantity",
                 "coupon_start_time", "coupon_end_time", "promotion_rate", "goods_eval_score", "goods_eval_count",
                 "cat_id", "avg_desc", "avg_lgst", "avg_serv", "desc_pct", "lgst_pct", "serv_pct"]


class GoodsVo:

    def __init__(self, goods_dict):
        self.create_at = goods_dict.get("create_at", None)
        self.goods_id = goods_dict.get("goods_id", None)
        self.goods_name = goods_dict.get("goods_name", None)
        self.goods_desc = goods_dict.get("goods_desc", None)
        self.goods_thumbnail_url = goods_dict.get("goods_thumbnail_url", None)
        self.goods_image_url = goods_dict.get("goods_image_url", None)
        self.goods_gallery_urls = goods_dict.get("goods_gallery_urls", None)
        self.sold_quantity = goods_dict.get("sold_quantity", None)
        self.min_group_price = goods_dict.get("min_group_price", None)
        self.min_normal_price = goods_dict.get("min_normal_price", None)
        self.mall_name = goods_dict.get("mall_name", None)
        self.merchant_type = goods_dict.get("merchant_type", None)
        self.category_id = goods_dict.get("category_id", None)
        self.category_name = goods_dict.get("category_name", None)
        self.opt_id = goods_dict.get("opt_id", None)
        self.opt_name = goods_dict.get("opt_name", None)
        self.opt_ids = goods_dict.get("opt_ids", None)
        self.cat_ids = goods_dict.get("cat_ids", None)
        self.mall_cps = goods_dict.get("mall_cps", None)
        self.has_coupon = goods_dict.get("has_coupon", None)
        self.coupon_min_order_amount = goods_dict.get("coupon_min_order_amount", None)
        self.coupon_discount = goods_dict.get("coupon_discount", None)
        self.coupon_total_quantity = goods_dict.get("coupon_total_quantity", None)
        self.coupon_remain_quantity = goods_dict.get("coupon_remain_quantity", None)
        self.coupon_start_time = goods_dict.get("coupon_start_time", None)
        self.coupon_end_time = goods_dict.get("coupon_end_time", None)
        self.promotion_rate = goods_dict.get("promotion_rate", None)
        self.goods_eval_score = goods_dict.get("goods_eval_score", None)
        self.goods_eval_count = goods_dict.get("goods_eval_count", None)
        self.cat_id = goods_dict.get("cat_id", None)
        self.avg_desc = goods_dict.get("avg_desc", None)
        self.avg_lgst = goods_dict.get("avg_lgst", None)
        self.avg_serv = goods_dict.get("avg_serv", None)
        self.desc_pct = goods_dict.get("desc_pct", None)
        self.lgst_pct = goods_dict.get("lgst_pct", None)
        self.serv_pct = goods_dict.get("serv_pct", None)


class Pid:
    def __init__(self, p_id_name, p_id):
        self.p_id_name = p_id_name
        self.p_id = p_id


class PromotionInfo:
    def __init__(self, promotion_dict):
        self.we_app_web_view_short_url = promotion_dict.get("we_app_web_view_short_url", None)
        self.we_app_web_view_url = promotion_dict.get("we_app_web_view_url", None)
        self.mobile_short_url = promotion_dict.get("mobile_short_url", None)
        self.mobile_url = promotion_dict.get("mobile_url", None)
        self.short_url = promotion_dict.get("short_url", None)
        self.url = promotion_dict.get("url", None)

        if "we_app_info" in promotion_dict.keys():
            self.we_app_icon_url = promotion_dict.get("we_app_info").get("we_app_icon_url", None)
            self.banner_url = promotion_dict.get("we_app_info").get("banner_url", None)
            self.desc = promotion_dict.get("we_app_info").get("desc", None)
            self.source_display_name = promotion_dict.get("we_app_info").get("source_display_name", None)
            self.page_path = promotion_dict.get("we_app_info").get("page_path", None)
            self.user_name = promotion_dict.get("we_app_info").get("user_name", None)
            self.title = promotion_dict.get("we_app_info").get("title", None)
            self.app_id = promotion_dict.get("we_app_info").get("app_id", None)
