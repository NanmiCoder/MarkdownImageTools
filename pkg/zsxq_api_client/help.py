# -*- coding: utf-8 -*-
import utils

def generate_x_signature(req_url: str, timestamp: str, request_id: str) -> str:
    """
    生成知识星球的X-Signature签名
    :param req_url:
    :param timestamp:
    :param request_id:
    :return:
    """
    return utils.sha1_encrypt(f"{req_url} {timestamp} {request_id}")

def generate_x_request_id() -> str:
    """
    生成X-Request-Id
    :return:
    """
    return utils.genarate_fake_uuid()