# Copyright (C) 2015-2020 ycmd contributors
#
# This file is part of ycmd.
#
# ycmd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ycmd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ycmd.  If not, see <http://www.gnu.org/licenses/>.

from hamcrest import ( assert_that,
                       calling,
                       empty,
                       has_entries,
                       has_items,
                       raises )
from webtest import AppError

from ycmd.tests.cs import PathToTestFile, SharedYcmd, WrapOmniSharpServer
from ycmd.tests.test_utils import BuildRequest, CompletionEntryMatcher
from ycmd.utils import ReadFile


@SharedYcmd
def GetCompletions_DefaultToIdentifier_test( app ):
  filepath = PathToTestFile( 'testy', 'Program.cs' )
  with WrapOmniSharpServer( app, filepath ):
    contents = ReadFile( filepath )

    completion_data = BuildRequest( filepath = filepath,
                                    filetype = 'cs',
                                    contents = contents,
                                    line_num = 10,
                                    column_num = 7 )
    response_data = app.post_json( '/completions', completion_data ).json
    print( 'Response: ', response_data )
    assert_that(
      response_data,
      has_entries( {
        'completion_start_column': 4,
        'completions': has_items(
          CompletionEntryMatcher( 'Console', '[ID]' ),
        ),
        'errors': empty(),
      } ) )


@SharedYcmd
def GetCompletions_Basic_test( app ):
  filepath = PathToTestFile( 'testy', 'Program.cs' )
  with WrapOmniSharpServer( app, filepath ):
    contents = ReadFile( filepath )

    completion_data = BuildRequest( filepath = filepath,
                                    filetype = 'cs',
                                    contents = contents,
                                    line_num = 10,
                                    column_num = 12 )
    response_data = app.post_json( '/completions', completion_data ).json
    print( 'Response: ', response_data )
    assert_that(
      response_data,
      has_entries( {
        'completion_start_column': 12,
        'completions': has_items(
          CompletionEntryMatcher( 'CursorLeft',
                                  'CursorLeft',
                                  { 'kind': 'Property' } ),
          CompletionEntryMatcher( 'CursorSize',
                                  'CursorSize',
                                  { 'kind': 'Property' } ),
        ),
        'errors': empty(),
      } ) )


@SharedYcmd
def GetCompletions_Unicode_test( app ):
  filepath = PathToTestFile( 'testy', 'Unicode.cs' )
  with WrapOmniSharpServer( app, filepath ):
    contents = ReadFile( filepath )

    completion_data = BuildRequest( filepath = filepath,
                                    filetype = 'cs',
                                    contents = contents,
                                    line_num = 43,
                                    column_num = 26 )
    response_data = app.post_json( '/completions', completion_data ).json
    assert_that( response_data,
                 has_entries( {
                    'completion_start_column': 26,
                    'completions': has_items(
                      CompletionEntryMatcher( 'DoATest' ),
                      CompletionEntryMatcher( 'an_int' ),
                      CompletionEntryMatcher( 'a_unic??de' ),
                      CompletionEntryMatcher( '??????' ),
                    ),
                    'errors': empty(),
                  } ) )


@SharedYcmd
def GetCompletions_MultipleSolution_test( app ):
  filepaths = [ PathToTestFile( 'testy', 'Program.cs' ),
                PathToTestFile( 'testy-multiple-solutions',
                                'solution-named-like-folder',
                                'testy',
                                'Program.cs' ) ]
  for filepath in filepaths:
    with WrapOmniSharpServer( app, filepath ):
      contents = ReadFile( filepath )

      completion_data = BuildRequest( filepath = filepath,
                                      filetype = 'cs',
                                      contents = contents,
                                      line_num = 10,
                                      column_num = 12 )
      response_data = app.post_json( '/completions',
                                     completion_data ).json

      print( 'Response: ', response_data )
      assert_that(
        response_data,
        has_entries( {
          'completion_start_column': 12,
          'completions': has_items(
            CompletionEntryMatcher( 'CursorLeft',
                                    'CursorLeft',
                                    { 'kind': 'Property' } ),
            CompletionEntryMatcher( 'CursorSize',
                                    'CursorSize',
                                    { 'kind': 'Property' } ),
          ),
          'errors': empty(),
        } ) )


@SharedYcmd
def GetCompletions_PathWithSpace_test( app ):
  filepath = PathToTestFile( '?????????????????????? ??????????', 'Program.cs' )
  with WrapOmniSharpServer( app, filepath ):
    contents = ReadFile( filepath )

    completion_data = BuildRequest( filepath = filepath,
                                    filetype = 'cs',
                                    contents = contents,
                                    line_num = 9,
                                    column_num = 12 )
    response_data = app.post_json( '/completions', completion_data ).json
    print( 'Response: ', response_data )
    assert_that(
      response_data,
      has_entries( {
        'completion_start_column': 12,
        'completions': has_items(
          CompletionEntryMatcher( 'CursorLeft',
                                  'CursorLeft',
                                  { 'kind': 'Property' } ),
          CompletionEntryMatcher( 'CursorSize',
                                  'CursorSize',
                                  { 'kind': 'Property' } ),
        ),
        'errors': empty(),
      } ) )


@SharedYcmd
def GetCompletions_DoesntStartWithAmbiguousMultipleSolutions_test( app ):
  filepath = PathToTestFile( 'testy-multiple-solutions',
                             'solution-not-named-like-folder',
                             'testy', 'Program.cs' )
  contents = ReadFile( filepath )
  event_data = BuildRequest( filepath = filepath,
                             filetype = 'cs',
                             contents = contents,
                             event_name = 'FileReadyToParse' )

  assert_that(
    calling( app.post_json ).with_args( '/event_notification', event_data ),
    raises( AppError, 'Autodetection of solution file failed' ),
    "The Omnisharp server started, despite us not being able to find a "
    "suitable solution file to feed it. Did you fiddle with the solution "
    "finding code in cs_completer.py? Hopefully you've enhanced it: you need "
    "to update this test then :)" )


def Dummy_test():
  # Workaround for https://github.com/pytest-dev/pytest-rerunfailures/issues/51
  assert True
