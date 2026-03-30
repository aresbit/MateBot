#### 9.5.1 Private Access Modifier

The modifier private indicates that a class member or a constructor is accessible (see Accessible) within its declaring class, i.e., a private member or constructor m declared in some class C can be accessed only within the class body of C:

class C {
    private count: number
    getCount(): number {
        return this.count // ok
    }
}

function increment(c: C) {
    c.count++ // compile-time error - 'count' is private
}

#### 9.5.2 Protected Access Modifier

The modifier protected indicates that a class member or a constructor is accessible (see Accessible) only within its declaring class and the classes derived from that declaring class. A protected member M declared in some class C can be accessed only within the class body of C or of a class derived from C:

class C {
    protected count: number
        getCount(): number {
            return this.count // ok
        }
}

class D extends C {
    increment() {
        this.count++ // ok, D is derived from C
    }
}

function increment(c: C) {
    c.count++ // compile-time error - 'count' is not accessible
}

#### 9.5.3 Public Access Modifier

The modifier public indicates that a class member or a constructor can be accessed everywhere, provided that the member or the constructor belongs to a type that is also accessible (see Accessible).
