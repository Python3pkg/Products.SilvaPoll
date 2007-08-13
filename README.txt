Copyright (c) 2006-2007 Infrae. All rights reserved.
See also LICENSE.txt

Meta::

  Valid for:  SilvaPoll 0.3.x
  Authors:    Guido Wesdorp, Wim Boucquaert, Jasper Op De Coul
  Email:      guido@infrae.com, wim@infrae.com, jasper@infrae.com

SilvaPoll
---------

SilvaPoll is an extension to have traditional polls inside Silva sites. A
question is asked on which the public can answer, and results are displayed
to those that do.

Installation
------------

For installation instructions, see INSTALL.txt.

Making a Poll
------------

Creating Silva Poll Questions
=============================
After following the installation instructions you can add a Silva Poll Question
in the SMI. Fill in all required fields and save the question, repeat this step
for all questions. Don't forget to separate possible answers by a blank line.

Rendering the Silva Poll
========================
Make a new Silva Document and click on external sources and add all
of your questions (don't forget to hit the "add external source" button ;-).

- rendering the poll immediately:
Publish your Silva Poll Questions and Silva Document and that's it.

- rendering time based Silva Poll Questions and their result:
Go to the SMI and go to the publish tab of a Silva Poll Question

Fill in the options you would like to set:
* question display start time: time when a Silva Poll Question should be
displayed for the public

* question display end time: time when a Silva Poll Question should stop being
displayed for the public

* results display start time: time when the result of Silva Poll Question should
be displayed for the public

* results display end time: time when the result of Silva Poll Question should
stop being displayed for the public

How-to stop rendering the Silva Poll Questions in the TOC (Table Of Contents)
=============================================================================
By default Silva Poll Questions are not hidden for the TOC. As navigation
the navigation of Silva relies on TOC they will be shown by default there.

There are 2 ways on how to avoid this:
1) The most time intensive one:
Go to the properties (tab_metadata) of a closes question and set the option
"hide from tables of content" to hide.
You have to repeat this step for every question you want to hide.

2) The time saver, more advanced way:
People who never want to show Silva Poll Questions in the navigation (TOC) can
do this by changing the code that creates the navigation in layout_macro.html.
eg get_public_tree.py
You can add a condition there to not show an OBJECT of
the metatype "Silva Poll Question"
OBJECT.meta_type == 'Silva Poll Question'

eg
def get_tree_html(node, endobj):
    tree = ''
    endpath = endobj.getPhysicalPath()
    for OBJECT in node.get_ordered_publishables():
        if not OBJECT.is_published():
            continue
        if OBJECT.get_metadata_element(
            'silva-extra', 'hide_from_tocs') == 'hide' or
            OBJECT.meta_type == 'Silva Poll Question':
            continue
            ...

ZODB product
------------
SilvaPoll questions refer to a SilvaPollService stored in the ZODB. It is
important therefore not to delete the service as existing polls will break then.

Contact information
-------------------

For questions, bug reports, etc. send email to guido@infrae.com, wim@infrae.com, jasper@infrae.com.
