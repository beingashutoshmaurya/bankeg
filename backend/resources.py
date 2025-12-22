# # from flask import current_app as app
# from flask_restful import Api, Resource, reqparse 
# # In route, we used request.get_json(), here, we are using reqparse is required to define what 
# # details/ attributes we want to extract from the request body
# from models import *
# # from flask_security import current_user, auth_required, roles_required, roles_accepted
# # from .util_funcs import roles_list

# api = Api()

# # customer - create issue, get issues details
# # Employee - update_task (pending -> complete), update issue
# # Manager - create_task, task_details, performance_details

# task_parser = reqparse.RequestParser()
# task_parser.add_argument('name')
# task_parser.add_argument('employee_id')
# task_parser.add_argument('customer_id')
# task_parser.add_argument('due_date')
# task_parser.add_argument('priority')
# task_parser.add_argument('description')

# class TaskApi(Resource):
#     # @auth_required('token')
#     # @roles_accepted('admin','manager')
#     def post(self):
#         try:
#             args = task_parser.parse_args()
#             assigned_date = datetime.strptime(args["due_date"], "%Y-%m-%d").date()

#             task = Task(title = args["name"],
#                         customer_id = args["customer_id"],
#                         employee_id = args["employee_id"],
#                         status = "Pending",
#                         due_date = assigned_date,
#                         priority = args["priority"],
#                         description = args["description"])
#             db.session.add(task)
#             db.session.commit()
#             return {
#                 "message": "Task created successfully"
#             }, 201
        
#         except:
#             return {
#                 "message": "All fields are not provided or the task provided already exists"
#             }, 400



#     # @auth_required('token')
#     # @roles_accepted('admin', 'manager')
#     def get(self): 
        
#         tasks = [] # stores list of objects of class Subject
#         task_jsons = []
#         tasks = Task.query.all()
#         # convering every object of class Subject into a disctionary
#         for task in tasks:
#             this_task = {}
#             this_task["id"] = task.id
#             this_task["name"] = task.title
#             this_task["priority"] = task.priority
#             this_task["customer"] = task.customer.full_name
#             this_task["employee"] = task.bank_employee.name
#             this_task["due_date"] = task.due_date.isoformat()
#             this_task["status"] = task.status

#             task_jsons.append(this_task)
#         if task_jsons:
#             return task_jsons, 201
#         else:
#             return {
#                 "message": "No tasks found"
#             }, 404
        

    
#     # @auth_required('token')
#     # @roles_required('employee')
    
#     def put(self, task_id):
#         task = Task.query.filter(Task.id == task_id).first()
#         if task:
#             task.status = "complete"
#             db.session.commit()
#             return {
#                 "message": "The task status updated successfully"
#             }, 201

#         else:
#             return {
#                 "message": "The task does not exist"
#             }, 404
        

# api.add_resource(TaskApi, '/api/task/get', '/api/task/create', '/api/task/update/<int:task_id>')






# issue_parser = reqparse.RequestParser()
# issue_parser.add_argument('title')  
# issue_parser.add_argument('customer_id')
# issue_parser.add_argument('description')

# class IssueApi(Resource):
#     # @auth_required('token')
#     # @roles_accepted('customer')
#     def post(self):
#         try:
#             args = issue_parser.parse_args()
#             issue = Issue(title = args["title"],
#                         customer_id = args["customer_id"],
#                         description = args["description"])
#             db.session.add(issue)
#             db.session.commit()
#             return {
#                 "message": "Issue created successfully"
#             }, 201
        
#         except:
#             return {
#                 "message": "All fields are not provided or the issue provided already exists"
#             }, 400
        

#     # @auth_required('token')
#     # @roles_accepted('admin', 'manager')
#     def get(self): 
#         issues = [] 
#         issue_jsons = []
#         issues = Issue.query.all()
        
#         for issue in issues:
#             this_issue = {}
#             this_issue["title"] = issue.title
#             this_issue["customer_id"] = issue.customer_id
#             this_issue["description"] = issue.description
#             this_issue["created_date"] = issue.assigned_date.isoformat() 

#             issue_jsons.append(this_issue)
#         if issue_jsons:
#             return issue_jsons, 201
#         else:
#             return {
#                 "message": "No issues found"
#             }, 404
    
#     # @auth_required('token')
#     # @roles_required('employee')
    
#     def put(self, issue_id):
#         issue = Issue.query.filter(Issue.id == issue_id).first()
#         if issue:
#             issue.status = "complete"
#             db.session.commit()
#             return {
#                 "message": "The issue status updated successfully"
#             }, 201

#         else:
#             return {
#                 "message": "The issue does not exist"
#             }, 404


# api.add_resource(IssueApi, '/api/issue/get', '/api/issue/create', '/api/issue/update/<int:issue_id>')


from flask import current_app as app
from flask_restful import Api, Resource, reqparse 
from models import *
# from flask_security import current_user, auth_required, roles_required, roles_accepted  # Not used, commented out

api = Api()

task_parser = reqparse.RequestParser()
task_parser.add_argument('name')
task_parser.add_argument('employee_id')
task_parser.add_argument('customer_id')
task_parser.add_argument('due_date')
task_parser.add_argument('priority')
task_parser.add_argument('description')

class TaskApi(Resource):
    def post(self):
        try:
            args = task_parser.parse_args()
            assigned_date = datetime.strptime(args["due_date"], "%Y-%m-%d").date()

            task = Task(title = args["name"],
                        customer_id = args["customer_id"],
                        employee_id = args["employee_id"],
                        status = "Pending",
                        due_date = assigned_date,
                        priority = args["priority"],
                        description = args["description"])
            db.session.add(task)
            db.session.commit()
            return {
                "message": "Task created successfully"
            }, 201
        
        except Exception as e:
            return {
                "message": f"Error: {str(e)}"
            }, 400

    def get(self): 
        tasks = []
        task_jsons = []
        tasks = Task.query.all()
        
        for task in tasks:
            this_task = {}
            this_task["id"] = task.id
            this_task["name"] = task.title
            this_task["priority"] = task.priority
            
            # Safe handling of relationships
            this_task["customer"] = task.customer.full_name if task.customer else "N/A"
            this_task["employee"] = task.bank_employee.name if task.bank_employee else "N/A"
            this_task["customer_id"] = task.customer_id
            this_task["employee_id"] = task.employee_id
            
            this_task["due_date"] = task.due_date.isoformat()
            this_task["status"] = task.status

            task_jsons.append(this_task)
            
        if task_jsons:
            return task_jsons, 200
        else:
            return {
                "message": "No tasks found"
            }, 404
    
    def put(self, task_id):
        task = Task.query.filter(Task.id == task_id).first()
        if task:
            task.status = "complete"
            db.session.commit()
            return {
                "message": "The task status updated successfully"
            }, 200

        else:
            return {
                "message": "The task does not exist"
            }, 404
        
api.add_resource(TaskApi, '/api/task/get', '/api/task/create', '/api/task/update/<int:task_id>')


issue_parser = reqparse.RequestParser()
issue_parser.add_argument('title')  
issue_parser.add_argument('customer_id')
issue_parser.add_argument('description')

class IssueApi(Resource):
    def post(self):
        try:
            args = issue_parser.parse_args()
            issue = Issue(title = args["title"],
                        customer_id = args["customer_id"],
                        description = args["description"])
            db.session.add(issue)
            db.session.commit()
            return {
                "message": "Issue created successfully"
            }, 201
        
        except Exception as e:
            return {
                "message": f"Error: {str(e)}"
            }, 400

    def get(self): 
        from flask import request
        customer_id = request.args.get('customer_id', type=int)
        
        issues = []
        issue_jsons = []
        
        if customer_id:
            issues = Issue.query.filter_by(customer_id=customer_id).all()
        else:
            issues = Issue.query.all()
        
        for issue in issues:
            this_issue = {}
            this_issue["id"] = issue.id
            this_issue["title"] = issue.title
            this_issue["customer_id"] = issue.customer_id
            this_issue["description"] = issue.description
            this_issue["created_date"] = issue.assigned_date.isoformat()
            this_issue["status"] = issue.status
            this_issue["resolution_summary"] = issue.resolution_summary if issue.resolution_summary else None
            # Email is considered sent if status is Complete and resolution_summary exists
            this_issue["emailSent"] = (issue.status and issue.status.lower() in ['complete', 'resolved']) and (issue.resolution_summary is not None)

            issue_jsons.append(this_issue)
            
        if issue_jsons:
            return issue_jsons, 200
        else:
            return {
                "message": "No issues found"
            }, 404
    
    def put(self, issue_id):
        issue = Issue.query.filter(Issue.id == issue_id).first()
        if issue:
            issue.status = "complete"
            db.session.commit()
            return {
                "message": "The issue status updated successfully"
            }, 200
        else:
            return {
                "message": "The issue does not exist"
            }, 404

api.add_resource(IssueApi, '/api/issue/get', '/api/issue/create', '/api/issue/update/<int:issue_id>')