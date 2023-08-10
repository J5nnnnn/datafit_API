class Classifer(Resource):
    # decorator for classifying
	@token_required
	def post(self, current_user):
		current_user = g.current_user  # access the current user with g.current_user
		if request.is_json:
				args = request.get_json()
				products_name = [x.lower() for x in args['data']]
				print(products_name)

				t1 = time.time()

				res = payload_preprocessing(model, model_sub, products_name)
				t2 = time.time()
				print(res)
				return json.dumps(res)
		else:
				return "Invalid payload format", 400



api.add_resource(Classifer, '/classify')