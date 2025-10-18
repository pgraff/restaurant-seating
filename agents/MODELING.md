We're working on building a specification in the @spec/ directory in markdown files.

here are some rules:
* We want to an abstract data model first
  * Use UML
  * Use non-directed associations
  * Use mermaid to visualize the models

## Mermaid Class Diagram Syntax Guidelines

When creating UML class diagrams with Mermaid, follow these syntax rules:

### Class Definition
```mermaid
class ClassName {
    +String attributeName
    -Integer privateAttribute
    #String protectedAttribute
}
```

### Relationship Syntax
- **One-to-Many**: `ClassA "1" -- "*" ClassB`
- **One-to-One**: `ClassA "1" -- "1" ClassB`
- **Many-to-Many**: `ClassA "*" -- "*" ClassB`
- **Zero or One**: `ClassA "0..1" -- "1" ClassB`
- **One or Many**: `ClassA "1" -- "1..*" ClassB`

### Important Notes
- Use quotes around cardinality notation: `"1"`, `"*"`, `"0..1"`, `"1..*"`
- Relationship labels are optional: `ClassA "1" -- "*" ClassB : label`
- **For conceptual models**: Use `--` for non-directed associations (bidirectional)
- **For implementation models**: Use `-->` for directed relationships if needed
- Cardinality notation: `1` for one, `*` for many, `0..1` for zero or one, `1..*` for one or many
- **Think carefully about cardinality**: Consider the business logic - can entities exist independently?
- **Avoid redundant relationships**: Don't duplicate the same association in both directions
- **Entity descriptions should focus on data only**: Describe what the entity represents and contains, not what it does or manages
- **Separate concerns**: Keep data model separate from responsibilities - responsibilities belong in services
- Always test Mermaid syntax before finalizing documentation

Please do not add fluffy comments. Focus on the task only.