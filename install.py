from Products.Silva.install import add_fss_directory_view
from Globals import package_home
import os

def install(root):
    add_fss_directory_view(root.service_views, 'SilvaPoll', __file__, 'views')
    add_fss_directory_view(root.service_resources, 'SilvaPoll', __file__, 'resources')
    registerViews(root.service_view_registry)
    setupMetadata(root)
    #configureSecurity(root)

def uninstall(root):
    unregisterViews(root.service_view_registry)
    root.service_views.manage_delObjects(['SilvaPoll'])
    root.service_resources.manage_delObjects(['SilvaPoll'])

def is_installed(root):
    return hasattr(root.service_views, 'SilvaPoll')

def registerViews(reg):
    reg.register('edit', 'Silva Poll Question',
                    ['edit', 'Content', 'PollQuestion'])
    reg.register('add', 'Silva Poll Question',
                    ['add', 'PollQuestion'])
    reg.register('public', 'Silva Poll Question',
                    ['public', 'PollQuestion'])

def unregisterViews(reg):
    """Unregister core views on registry.
    """
    reg.unregister('edit', 'Silva Poll Question')
    reg.unregister('public', 'Silva Poll Question')
    reg.unregister('add', 'Silva Poll Question')

def setupMetadata(root):
    silvapoll_home = package_home(globals())
    silvapoll_docs = os.path.join(silvapoll_home, 'doc')
    
    collection = root.service_metadata.getCollection()
    if 'silvapolls-date' in collection.objectIds():
        collection.manage_delObjects(['silvapolls-date'])

    xml_file = os.path.join(silvapoll_docs, 'silvapolls-date.xml')
    fh = open(xml_file, 'r')        
    collection.importSet(fh)

    root.service_metadata.addTypesMapping(['Silva Poll Question'],
                                            ('silva-content', 'silva-extra',
                                                'silvapolls-date'))
    return
    mapping = root.service_metadata.getTypeMapping()
    default = ''
    tm = (
            {'type': 'Silva Poll Question', 
                'chain': 'silva-content, silva-extra, silvapolls-date'},
        )
        
    mapping.editMappings(default, tm)

