import sys
from datetime import datetime
from datetime import timedelta
from pyral import Rally, rallyWorkset

##########################################################################################
#
# Edit these variables
#
##########################################################################################
# What do you want to search for?
search_string = "my search string"

# How many weeks back would you like to go?
weeks_max = 275

##########################################################################################

options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
args = [arg for arg in sys.argv[1:] if arg not in options]

server, user, password, apikey, workspace, project = rallyWorkset(options)

rally = Rally(server, user, password, workspace=workspace, project=project)
rally.enableLogging(dest=b'rallylog.log', attrget=True)

y = 0
end_date = datetime.now().date()
start_date = end_date - timedelta(weeks=1)

while y < weeks_max:
    query = '(((Description CONTAINS "{search_string}") AND (CreationDate >= "{start_date}")) AND (CreationDate <= "{end_date}"))'.format(search_string=search_string,start_date=start_date,end_date=end_date)
    revisions = rally.get('Revision', fetch='CreationDate,Description,User,UserName,RevisionHistory', query=query)
    if revisions.resultCount > 0:
        for revision in revisions:
            if search_string in revision.Description:
                print("CreationDate: {creation_date}, User: {user_name}, Description: {description}, RevisionHistory: {revision_history}".format(creation_date=revision.CreationDate, user_name=revision.User.UserName, description=revision.Description, revision_history=revision.RevisionHistory._ref))

    end_date = end_date - timedelta(weeks=1)
    start_date = end_date - timedelta(weeks=1)

    y = y + 1
