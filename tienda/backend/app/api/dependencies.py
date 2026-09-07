from app.application.use_cases import CustomerUseCases, OrderUseCases, ProductUseCases
from app.infrastructure.mongo_repositories import MongoCustomerRepository, MongoOrderRepository, MongoProductRepository


def get_product_use_cases() -> ProductUseCases:
    return ProductUseCases(MongoProductRepository())


def get_customer_use_cases() -> CustomerUseCases:
    return CustomerUseCases(MongoCustomerRepository())


def get_order_use_cases() -> OrderUseCases:
    return OrderUseCases(MongoOrderRepository(), MongoProductRepository(), MongoCustomerRepository())
