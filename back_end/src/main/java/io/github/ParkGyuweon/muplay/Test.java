package io.github.ParkGyuweon.muplay;

import org.python.util.PythonInterpreter;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import lombok.RequiredArgsConstructor;
import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyInteger;
@RestController
@RequiredArgsConstructor

public class Test {
    private static PythonInterpreter intPre;

    @RequestMapping(value = "/test", method = RequestMethod.GET)
    public String getTest() {

        // python 함수로 확인
        intPre = new PythonInterpreter();
        intPre.execfile("src/main/java/io/github/ParkGyuweon/muplay/test.py");

        PyFunction pyFunction = (PyFunction) intPre.get("testFunc", PyFunction.class);
        int a = 10, b = 20;
        PyObject pyobj = pyFunction.__call__(new PyInteger(a), new PyInteger(b));
        System.out.println(pyobj.toString());

        return pyobj.toString();
    }
}