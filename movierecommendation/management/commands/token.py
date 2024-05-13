import requests
import json


def main():
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Ut1gM920uAh54jssmR9FEBVa&client_secret=YYZ0dlnyJwmvKbGn5QT4apbBtMaDr2oh"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

{
    "refresh_token":"25.9e7db856ce0ac22ab4dc1cfe9bf33bdd.315360000.2030974433.282335-70276673",
    "expires_in":2592000,"session_key":"9mzdDorF84KTYsILnpoHBTIoS4VYGapg0a62AuU7u8NlPcQlnAYCXCicCmMJgZQkZbPkMFhNx1tx+gTWDqEwa9eSS7h2+Q==",
    "access_token":"24.583bfe8e8b55415de7b5c59bb76f6016.2592000.1718206433.282335-70276673",
    "scope":"public ai_custom_qianfan_bloomz_7b_compressed ai_custom_yiyan_com ai_custom_yiyan_com_ai_apaas ai_custom_yiyan_com_aquilachat_7b ai_custom_yiyan_com_bce_reranker_base ai_custom_yiyan_com_bloomz7b1 ai_custom_yiyan_com_chatglm2_6b_32k ai_custom_yiyan_com_chatlaw ai_custom_yiyan_com_codellama_7b_ins ai_custom_yiyan_com_eb_instant ai_custom_yiyan_com_eb_pro ai_custom_yiyan_com_eb_pro_prmtv ai_custom_yiyan_com_eb_turbo_pro ai_custom_yiyan_com_eb_turbo_pro_128k ai_custom_yiyan_com_emb_bge_large_en ai_custom_yiyan_com_emb_bge_large_zh ai_custom_yiyan_com_emb_tao_8k ai_custom_yiyan_com_emb_text ai_custom_yiyan_com_ernie_35_4k_0205 ai_custom_yiyan_com_ernie_35_8k_0205 ai_custom_yiyan_com_ernie_35_8k_0329 ai_custom_yiyan_com_ernie_35_8k_1222 ai_custom_yiyan_com_ernie_35_8k_preview ai_custom_yiyan_com_ernie_40_8k_0104 ai_custom_yiyan_com_ernie_40_8k_0329 ai_custom_yiyan_com_ernie_40_8k_preview ai_custom_yiyan_com_ernie_char_8k ai_custom_yiyan_com_ernie_func_8k ai_custom_yiyan_com_ernie_lite_8k ai_custom_yiyan_com_ernie_tiny_8k ai_custom_yiyan_com_fuyu_8b ai_custom_yiyan_com_gemma_7b_it ai_custom_yiyan_com_llama2_13b ai_custom_yiyan_com_llama2_70b ai_custom_yiyan_com_llama2_7b ai_custom_yiyan_com_llama3_70b ai_custom_yiyan_com_llama3_8b ai_custom_yiyan_com_mixtral_8x7b ai_custom_yiyan_com_prmtv ai_custom_yiyan_com_qf_chinese_llama_2_13b ai_custom_yiyan_com_qianfan_chinese_llama_2_7b ai_custom_yiyan_com_sd_xl ai_custom_yiyan_com_sqlcoder_7b ai_custom_yiyan_com_tokenizer_eb ai_custom_yiyan_com_xuanyuan_70b_chat ai_custom_yiyan_com_yi_34b brain_all_scope wenxinworkshop_mgr wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test\u6743\u9650 vis-classify_flower lpq_\u5f00\u653e cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base smartapp_mapp_dev_manage iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey smartapp_swanid_verify smartapp_opensource_openapi smartapp_opensource_recapi fake_face_detect_\u5f00\u653eScope vis-ocr_\u865a\u62df\u4eba\u7269\u52a9\u7406 idl-video_\u865a\u62df\u4eba\u7269\u52a9\u7406 smartapp_component smartapp_search_plugin avatar_video_test b2b_tp_openapi b2b_tp_openapi_online smartapp_gov_aladin_to_xcx","session_secret":"cbaea767e3f1a27fa99e352b5c22b324"
}



if __name__ == '__main__':
    main()