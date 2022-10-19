
class LabCrmPipline:
    def home_dashboard(self, lab_id):
        pipline = [
            {
                '$match': {
                    'id': lab_id
                }
            }
            ,{
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
                        }, {
                            '$limit': 10
                        }
                    ], 
                    'as': 'recent_bookings'
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
                                }, 
                                'status': 'NEW'
                            }
                        }, {
                            '$sort': {
                                'created_at': -1
                            }
                        }, {
                            '$project': {
                                '_id': 0
                            }
                        }, {
                            '$group': {
                                '_id': None, 
                                'count': {
                                    '$sum': 1
                                }
                            }
                        }
                    ], 
                    'as': 'new_booking_count'
                }
            }, {
                '$unwind': {
                    'path': '$new_booking_count'
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
                                }, 
                                'status': 'COMPLETE'
                            }
                        }, {
                            '$sort': {
                                'created_at': -1
                            }
                        }, {
                            '$project': {
                                '_id': 0
                            }
                        }, {
                            '$group': {
                                '_id': None, 
                                'count': {
                                    '$sum': 1
                                }
                            }
                        }
                    ], 
                    'as': 'completed_booking_count'
                }
            }, {
                '$unwind': {
                    'path': '$completed_booking_count'
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
                                }, 
                                'status': 'PROCESSED'
                            }
                        }, {
                            '$sort': {
                                'created_at': -1
                            }
                        }, {
                            '$project': {
                                '_id': 0
                            }
                        }, {
                            '$group': {
                                '_id': None, 
                                'count': {
                                    '$sum': 1
                                }
                            }
                        }
                    ], 
                    'as': 'processed_booking_count'
                }
            }, {
                '$unwind': {
                    'path': '$processed_booking_count'
                }
            }, {
                '$project': {
                    'name': 1, 
                    'icon': 1, 
                    'id': 1, 
                    'recent_bookings': 1, 
                    'new_booking_count': '$new_booking_count.count', 
                    'completed_booking_count': '$completed_booking_count.count', 
                    'processed_booking_count': '$processed_booking_count.count'
                }
            }
        ]
        return pipline

LabCrmPiplineServies = LabCrmPipline()