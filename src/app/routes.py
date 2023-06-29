from fastapi import APIRouter
from .endpoints.contas_a_pagar_e_receber import router as contas_pagar
from .endpoints.fornecedor_cliente import router as fornec
from .endpoints.fornecedor_cliente_contas import router as fornec_cont

router = APIRouter()
router.include_router(contas_pagar)
router.include_router(fornec)
router.include_router(fornec_cont)
