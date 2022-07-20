def test_example(new_user):
    user = new_user
    print(user.username)
    assert True if user.username else False


# def test_customer(new_customer):
#     customer = new_customer
#     print(customer.first_name)
#     assert True if customer.user.username else False

