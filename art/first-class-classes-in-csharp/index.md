---
category: etc
date: '2011-04-28'
layout: article
redirect_from: '/etc/first-class-classes-in-csharp/'
slug: 'first-class-classes-in-csharp'
tags:
    - c
    - functional-programming
title: '(sort of) First Class Classes in C#'
summary: It seems, at first, that C# doesn't have first-class classes.  But ...
---

I find myself writing some C\# code while still thinking in Python. One
thing in particular caught me out … it seems, at first, that C\# doesn’t
have first class classes. This is annoying, because I’d started writing
some device driver classes where each class is a type of device, and
instances represent the individual devices themselves. And I wanted to
construct a list of these classes, and call a “probe” classmethod on
each of them to ask the class to go search out any devices which were
available. In Python, this would look like :

{% highlight python %}
device_classes = (FooDevice, BarDevice, BazDevice)

for device_class in device_classes:
    device_class.probe()
{% endhighlight %}

See? The classes are being treated just like any other variable, because
they are, they’re just instances of type ‘classobj’ . But the equivalent
doesn’t work in C\# — doing this:

{% highlight csharp %}
Type[] DeviceClasses = {
    FooDevice,
    BarDevice,
    BazDevice
};
{% endhighlight %}

... complains that “‘FooDevice’ is a ‘type’ but is used like a
‘variable’”. At first it seemed that C\# didn’t have first class
classes, and indeed a few web searches came up empty handed.

Thankfully after a bit more exploration it turns out that all that is
needed is some syntactic nastiness … namely, typeof(), GetMethod() and
Invoke() (Passing “null” to Invoke works for static methods):

{% highlight csharp %}
Type[] DeviceClasses = {
    typeof(FooDevice),
    typeof(BarDevice),
    typeof(BazDevice)
};

foreach (Type dct in DeviceClasses) {
    dct.GetMethod("Probe").Invoke(null, new object[] {} );
}
{% endhighlight %}


Now, quite why a shiny new programming language has to get saddled with
such godawful syntax is a bit beyond me, but so it goes.

As always, this is [lovingly documented in
MSDN](http://msdn.microsoft.com/en-us/library/6hy0h0z1.aspx), in such a
way that the answer is clear so long as you already know what you’re
looking for.

(As a bonus, yes, you can use reflection to find the list of Devices in
the first place. It just wasn’t all that relevant to this example)
