# Copyright 2024 University of Calgary
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Class definition for a metadata filter objects
"""

from typing import List, Literal, Union, Any


class MetadataFilterExpression:
    """
    Representation for an AuroraX search engine metadata filter expression. These are used 
    as part of conjunction, ephemeris, and data product searching.

    Attributes:
        key (str): 
            The special key for the metadata filter. For example, 'nbtrace_region'.
        
        values (Any or List[Any]): 
            The value(s) that the search will use when filtering. This can either be a single value, 
            or a list of values.

        operator (str): 
            The operator to use when the search engine evaluates the expression. Valid choices
            are: "=", "!=", ">", "<", ">=", "<=", "between", "in", "not in".

            The "in" and "not in" operators are meant exclusively for expressions where there 
            are multiple values (ie. the values parameter is a list of strings).
        
    Raises:
        ValueError: if invalid operator was specified.
    """

    def __init__(
        self,
        key: str,
        values: Union[Any, List[Any]],
        operator: Literal["=", "!=", ">", "<", ">=", "<=", "between", "in", "not in"] = "in",
    ):
        # set required parameters
        self.key = key
        self.values = values

        # set operator
        if (operator not in ["=", "!=", ">", "<", ">=", "<=", "between", "in", "not in"]):
            raise ValueError(
                "Operator '%s' not allowed. You must use one of the following: ['=', '!=', '>', '<', '>=', '<=', 'between', 'in', 'not in']" %
                (operator))
        self.__operator = operator

    @property
    def operator(self) -> str:
        return self.__operator

    @operator.setter
    def operator(self, val: Literal["=", "!=", ">", "<", ">=", "<=", "between", "in", "not in"]):
        if (val not in ["=", "!=", ">", "<", ">=", "<=", "between", "in", "not in"]):
            raise ValueError(
                "Operator '%s' not allowed. You must use one of the following: ['=', '!=', '>', '<', '>=', '<=', 'between', 'in', 'not in']" % (val))
        self.__operator = val

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        # set special strings
        values_str = "'%s'" % (self.values)
        if (type(self.values) is list):
            values_str = str(self.values)

        # return
        return "MetadataFilterExpression(key='%s', values=%s, operator='%s')" % (self.key, values_str, self.operator)

    def pretty_print(self):
        """
        A special print output for this class.
        """

        # print
        print("MetadataFilterExpression:")
        print("  %-10s: %s" % ("key", self.key))
        print("  %-10s: %s" % ("values", self.values))
        print("  %-10s: %s" % ("operator", self.operator))

    def to_query_dict(self):
        """
        Convert the expression object to a dictionary that will be used when executing a search.
        """
        return {
            "key": str(self.key),
            "values": [str(self.values)] if type(self.values) is not list else self.values,
            "operator": str(self.operator),
        }


class MetadataFilter:
    """
    Representation for an AuroraX search engine metadata filter. These are used 
    as part of conjunction, ephemeris, and data product searching.

    Attributes:
        expressions (List[MetadataFilterExpression]): 
            The list of metadata filter expressions for use with conjunction, ephemeris, and 
            data product searches.
        
        operator (str): 
            The logical operator to use when the search engine will evaluate multiple expressions. If 
            not supplied, the search engine will perform a logical 'AND' between each expression. Possible
            choices are 'and' or 'or'.

    Raises:
        ValueError: if invalid operator was specified.
    """

    def __init__(
        self,
        expressions: List[MetadataFilterExpression],
        operator: Literal["and", "or", "AND", "OR"] = "and",
    ):
        self.expressions = expressions

        # set operator
        if (operator.lower() not in ["and", "or"]):
            raise ValueError("Operator '%s' not allowed. You must use one of the following: ['and', 'or']" % (operator))
        self.__operator = operator

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    def operator(self, val: Literal["and", "or", "AND", "OR"] = "and"):
        if (val.lower() not in ["and", "or"]):
            raise ValueError("Operator '%s' not allowed. You must use one of the following: ['and', 'or']" % (val))
        self.__operator = val.lower()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        # set special strings
        if (len(self.expressions) == 1):
            expressions_str = "[1 expression]"
        else:
            expressions_str = "[%d expressions]" % (len(self.expressions))

        # return
        return "MetadataFilter(expressions=%s, operator='%s')" % (expressions_str, self.operator)

    def pretty_print(self):
        """
        A special print output for this class.
        """
        # set special strings
        if (len(self.expressions) == 1):
            expressions_str = "[1 expression]"
        else:
            expressions_str = "[%d expressions]" % (len(self.expressions))

        # print
        print("MetadataFilter:")
        print("  %-13s: %s" % ("expressions", expressions_str))
        print("  %-13s: %s" % ("operator", self.operator))

    def to_query_dict(self):
        """
        Convert the expression object to a dictionary that will be used when executing a search.
        """
        return {
            "expressions": [x.to_query_dict() for x in self.expressions],
            "logical_operator": self.operator.upper(),
        }
