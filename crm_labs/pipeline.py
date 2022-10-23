
class LabCrmPipline:
    def home_dashboard(self, lab_id):
        pipline = [
            {
                '$match': {
                    'id': lab_id
                }
            }, {
                '$lookup': {
                    'from': 'bookings', 
                    'let': {
                        'id': '$id'
                    }, 
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$eq': [
                                        '$lab_id', '$$id'
                                    ]
                                }
                            }
                        }, {
                            '$sort': {
                                'created_at': -1
                            }
                        }, {
                            '$project': {
                                '_id': 0
                            }
                        }
                    ], 
                    'as': 'bookings'
                }
            }, {
                '$project': {
                    'name': 1, 
                    'icon': 1, 
                    'id': 1, 
                    'bookings': 1
                }
            }
        ]
        return pipline

LabCrmPiplineServies = LabCrmPipline()