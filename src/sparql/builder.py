from typing import List

from src.sparql.rdf_namespaces import NamespaceProperty, SparqlFunctionString


class FromGraph:
    DATASETS = " FROM <https://datasets.fellesdatakatalog.digdir.no>"
    DATA_SERVICES = " FROM <https://dataservices.fellesdatakatalog.digdir.no>"
    ALL = ""


class SparqlFunction:
    def __init__(self, function: SparqlFunctionString, var: str, as_var):
        self.var = SparqlBuilder.make_var(var)
        self.function = function
        self.as_var = SparqlBuilder.make_var(as_var)

    def __str__(self):
        fun_str = f"{self.function}({self.var})"
        if self.as_var:
            fun_str += f" AS {self.as_var}"
        return fun_str


class SparqlGraphTerm:
    def __init__(self, var: str = None, namespace_property: str = None):
        if var:
            self.value = SparqlBuilder.make_var(var)
        if namespace_property:
            self.value = namespace_property

    @staticmethod
    def build_graph_pattern(subject: 'SparqlGraphTerm',
                            predicate: 'SparqlGraphTerm',
                            obj: 'SparqlGraphTerm',
                            close_pattern_with: str = None) -> str:
        graph_pattern = f"{subject.value} {predicate.value} {obj.value}"
        if close_pattern_with:
            graph_pattern += f" {close_pattern_with}"
        return graph_pattern


class SparqlSelect:

    def __init__(self, variable_names: List[str] = None, functions=None, from_graph: FromGraph = FromGraph.ALL):
        self.variable_names = variable_names
        self.functions = functions
        self.from_graph = from_graph

    def __str__(self):
        select_str = SparqlSelect.select(self.variable_names)
        if self.functions:
            for fun in self.functions:
                select_str += f" ({str(fun)})"
        return f"{select_str}{self.from_graph}"

    @staticmethod
    def select(variable_names: List[str] = None) -> str:
        select = "SELECT"
        if not variable_names:
            return f"{select} *"
        else:
            separator: str = " "
            if variable_names:
                sparql_vars = [SparqlBuilder.make_var(x) for x in variable_names]
                select += separator + separator.join(sparql_vars)
            return select


class SparqlWhere:
    def __init__(self, graphs: List[str] = None,
                 optional: 'SparqlOptional' = None, nested_clause: str = None):
        self.graph_patterns = graphs
        self.optional = optional
        self.nested_clause = nested_clause

    def __str__(self) -> str:
        return SparqlWhere.build(graphs=self.graph_patterns,
                                 optional_clause=self.optional,
                                 nested_clause_builder=self.nested_clause)

    @staticmethod
    def build(graphs: List[str] = None,
              build_as_optional: bool = False,
              optional_clause: 'SparqlOptional' = None,
              nested_clause_builder: 'SparqlBuilder' = None,
              ) -> str:
        if build_as_optional:
            where_str = "OPTIONAL { "
        else:
            where_str = "WHERE { "
        if graphs:
            for pattern in graphs:
                where_str += f"{pattern} "
        if optional_clause:
            where_str += f"{str(optional_clause)} "
        if nested_clause_builder:
            where_str += "{ "
            where_str += f"{nested_clause_builder.build()} "
            where_str += "} "
        if build_as_optional:
            where_str += "} "
        return where_str.strip()


class SparqlOptional(SparqlWhere):
    def __init__(self, graphs: List[str] = None, parent: 'SparqlWhere' = None):
        super().__init__(graphs, parent)

    def __str__(self) -> str:
        return SparqlWhere.build(graphs=self.graph_patterns, build_as_optional=True)


class SparqlBuilder:

    def __init__(self, prefix: List[NamespaceProperty] = None, select: SparqlSelect = None, where: SparqlWhere = None,
                 group_by_vars: List[str] = None, group_by_str: str = None, order_by_str=None):
        self.prefix = prefix
        self.select = select
        self.where = where
        if group_by_vars:
            self.group_by = " ".join([SparqlBuilder.make_var(v) for v in group_by_vars])
        elif group_by_str:
            self.group_by = group_by_str
        else:
            self.group_by = False
        if order_by_str:
            self.order_by = order_by_str
        else:
            self.order_by = False

    @staticmethod
    def make_var(var_str: str) -> str:
        if var_str.startswith("?"):
            return var_str
        else:
            return f"?{var_str}"

    def build(self):
        query_str = ""
        if self.prefix:
            for p in self.prefix:
                query_str += f"PREFIX {p.get_ttl_ns_definition()} "
        if self.select:
            query_str += f"{str(self.select)} "
        if self.where:
            query_str += f"{str(self.where)}"
            query_str += " } "
        if self.group_by:
            query_str += f"GROUP BY {self.group_by} "
        return query_str.strip()
