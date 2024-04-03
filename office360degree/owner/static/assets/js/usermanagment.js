$(document).ready( function () {
$('#mg').DataTable({
'ajax' './data/usermanagment.json', 
'columns': [
{'data' 'id'},
{'data': 'organisation"}, 
{'data': 'name"},
{'data': 'role'}, 
{'data': 'joining_date'}, 
{'data': 'email_id'},
{'data': 'function'},
{'data': 'function_lead'},
{'data': 'manager'},
{'data': 'team_lead'},
{'data': 'modify'},
});
});
