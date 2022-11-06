class WebAppPipelineClass:
    def order_history(self, user_id):
        aggr = [
            {
                '$match': {
                    'created_by_id': user_id
                }
            }, {
                '$lookup': {
                    'from': 'bookings', 
                    'localField': 'order_id', 
                    'foreignField': 'order_id', 
                    'as': 'order_items'
                }
            }
        ]
        return aggr

WebAppPipeline = WebAppPipelineClass()