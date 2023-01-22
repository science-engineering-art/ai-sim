from templates.models import BaseNode
     

def iter_fields(node: 'NodeVisitor'):
    for field in node.__dict__:
        try: 
            yield field, getattr(node, field)
        except:...


class NodeVisitor:
    """
        JSON Serializer
    """
    def visit(self, node: 'NodeVisitor'):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: 'NodeVisitor'):
        json = {}

        for key, value in iter_fields(node):
           
            if isinstance(value, list):
                json[key] = []
                for item in value:
                    if isinstance(item, BaseNode):
                        json[key].append(self.visit(item))
                    else:
                        json[key].append(item)
            
            elif isinstance(value, dict):
                if key not in json:
                    json[key] = {}
                for kw, item in value.items():
                    if isinstance(item, BaseNode):
                        if isinstance(kw, tuple):
                            x, y = kw
                            x, y = f"{x}", f"{y}"
                            if x not in json[key]:
                                json[key][x] = {}
                            if y not in json[key][x]:
                                json[key][x][y] = {}
                            json[key][x][y] = self.visit(item)
                        else:
                            json[key][kw] = self.visit(item)

            elif isinstance(value, BaseNode):
                json[key] = self.visit(value)

            else:
                json[key] = value

        return json
