<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Form of Interface Property</td><td style='text-align: center; word-wrap: break-word;'>Implementation in a Class</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>readonly field</td><td style='text-align: center; word-wrap: break-word;'>readonly field, field, getter, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>getter only</td><td style='text-align: center; word-wrap: break-word;'>readonly field, field, getter, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>field</td><td style='text-align: center; word-wrap: break-word;'>field, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>getter and setter</td><td style='text-align: center; word-wrap: break-word;'>field, or getter and setter</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>setter only</td><td style='text-align: center; word-wrap: break-word;'>field, setter, or setter and getter</td></tr></table>

Providing implementation for the property in the form of a field is not necessary:

interface Style {
    get color(): string
        set color(s: string)
    }

    class StyleClassOne implements Style {
        color: string = ""
    }

    class StyleClassTwo implements Style {
        private color_: string = ""

        get color(): string {
            return this.color_
        }

        set color(s: string) {
            this.color_ = s
        }
    }
}

If a property is implemented as a field, then any required accessors and a private hidden field are defined implicitly. Entities for StyleClassOne are implicitly defined as follows:

class StyleClassOne implements Style {
    private $$_color: string = "" // the exact name of the field is implementation_
    →specific
    get color(): string { return this.$$_color }
    set color(s: string) { this.$$_color = s }
}

If a property is defined in a form that requires a setter, then the implementation of the property in the form of a readonly field causes a compile-time error:

interface Style {
    set color(s: string)
        可可
        可可
    }

    class StyleClassTwo implements Style {
        readonly color: string = "" // compile-time error
        readonly writable: number = 0 // compile-time error
    }
}

(continues on next page)
