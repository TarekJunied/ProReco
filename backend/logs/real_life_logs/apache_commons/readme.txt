
-----

Apache Commons Crypto 1.0.0 - Stream CbcNopad Unit Test Software Event Log
Author			Leemans, M. (Maikel)

This software XES event log is obtained through the code instrumentation via the tool available at https://svn.win.tue.nl/repos/prom/XPort/. The following event attributes are used:

-----
	
Explanation for XES attributes:
	concept:name			The full package.class.method(params) name of the method executed
	time:timestamp			The timestamp (milliseconds) when the event was executed
	lifecycle:transition	Two possible values:
								start 		This event is a method call (start of a method interval)
								complete	This event is a method return (end of a method interval)
	org:resource			ID of the Java thread that generated this event
	apprun:threadid			ID of the Java thread that generated this event
	apploc:app				Constant name for the application name
	apploc:tier				Constant name for the application module
	apploc:node				Constant name for the application version
	apploc:etype			Extended version of the lifecycle:transition information. Possible values:
								call_new	Method call to a class constructor
								return_new	Method return from a class constructor
								call		Method call to a normal method
								return		Method return from a normal method
								throw		Method return in case of an exception
	apploc:filename			Sourcecode filename in which the executed method is defined
	apploc:linenr			Sourcecode line numer at which the executed method is defined
	apploc:joinpoint		Full package.class.method(params) joinpoint name of the method executed 
	apploc:regionstr		Not used
	apprun:nanotime			The value of the most precise available system timer, in nanoseconds, 
							when the event was executed. This can only be used to measure elapsed time 
							and is not related to any other notion of system or wall-clock time. 
	apprun:excatchtype		[optional] Java type of exception if caught, otherwise its <uncaught>
	apprun:exthrowtype		[optional] Java type of exception that is throwed (apploc:etype = throw)

-----

All three unit tests passed.