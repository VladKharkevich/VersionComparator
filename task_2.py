import functools
import re
from typing import List

word_to_number_version = {
    'a': '-3',
    'alpha': '-3',
    'b': '-2',
    'beta': '-2',
    'c': '-1',
    'rc': '-1',
}


@functools.total_ordering
class Version:
    def __init__(self, version):
        self.version = version

    def _is_lower(self, first_version: str, second_version: str) -> bool:
        first_version_list = self._validate(first_version)
        second_version_list = self._validate(second_version)
        return first_version_list < second_version_list

    def _is_equal(self, first_version: str, second_version: str) -> bool:
        first_version_list = self._validate(first_version)
        second_version_list = self._validate(second_version)
        return first_version_list == second_version_list

    def _validate(self, version: str) -> List[int]:
        """
            transform data like '1.0.4-alpha.beta to [1, 0, 4, -3, -2]'
        """
        list_version: List[str] = re.split(r"\.|-", version)
        list_version = self._validate_patch_version(list_version)
        for i in range(5 - len(list_version)):
            list_version.append('0')
        list_version = list(
            map(self._transform_word_version_to_number, list_version))
        return [int(elem) for elem in list_version]

    def _transform_word_version_to_number(self, version: str) -> str:
        return word_to_number_version.get(version, version)

    def _validate_patch_version(self, list_version: List[str]) -> List[str]:
        """
            Validate situations like 1.8.1b5 to 1.8.1.b.5
        """
        index_of_patch_version = 2
        index_of_pre_release_version = 3
        index_of_qualifier_version = 4

        if not list_version[index_of_patch_version].isdigit():
            expression = re.compile("([0-9]+)([a-z]+)([0-9]*)")
            match_groups = expression.match(
                list_version[index_of_patch_version])
            if match_groups:
                list_version[index_of_patch_version] = match_groups.group(1)
                list_version.insert(
                    index_of_pre_release_version, match_groups.group(2))
                if (match_groups.group(3) != ''):
                    list_version.insert(
                        index_of_qualifier_version, match_groups.group(3))
        return list_version

    def __eq__(self, other):
        return self._is_equal(self.version, other.version)

    def __lt__(self, other):
        return self._is_lower(self.version, other.version)


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]
    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
