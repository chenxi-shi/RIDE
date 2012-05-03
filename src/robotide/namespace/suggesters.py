#  Copyright 2008-2012 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


class SuggestionSource(object):

    def __init__(self, plugin, controller):
        self._plugin = plugin
        self._controller = controller

    def get_suggestions(self, value, row=None):
        if self._controller:
            return self._controller.get_local_namespace_for_row(row).get_suggestions(value)
        return self._plugin.content_assist_values(value) # TODO: Remove old functionality when no more needed


class _Suggester(object):

    def _suggestion(self, name):
        s = lambda:0
        s.name = name
        s.longname = name
        s.details = None
        return s


class HistorySuggester(_Suggester):

    def __init__(self):
        self._suggestions = []

    def get_suggestions(self, name, *args):
        return [s for s in self._suggestions if name is None or name in s.name]

    def store(self, name):
        self._suggestions += [self._suggestion(name)]
        self._suggestions.sort()


class _ImportSuggester(_Suggester):

    def __init__(self, controller):
        self._df_controller = controller.datafile_controller

    def get_suggestions(self, name, *args):
        already_imported = self._get_already_imported()
        all_resources = self._get_all_available()
        suggestion_names = all_resources - already_imported
        return [self._suggestion(n) for n in sorted(suggestion_names) if name in n]


class ResourceSuggester(_ImportSuggester):

    def _get_already_imported(self):
        return set(imp.name  for imp in self._df_controller.imports)

    def _get_all_available(self):
        return set(self._df_controller.relative_path_to(r) for r in self._df_controller._chief_controller.resources)


class LibrarySuggester(_ImportSuggester):

    def _get_already_imported(self):
        return set(imp.name  for imp in self._df_controller.imports)

    def _get_all_available(self):
        return set(l.name for l in self._df_controller._chief_controller.libraries)
