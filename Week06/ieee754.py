import numpy as np
import math

class IEEE754:
    def __init__(self, x: str, precision: int = 2,
                 force_length: int = None,
                 force_exponent: int = None,
                 force_mantissa: int = None,
                 force_bias: int = None):
        self.precision = precision
        length_list = [16, 32, 64, 128, 256, 512]
        exponent_list = [5, 8, 11, 15, 19]
        mantissa_list = [10, 23, 52, 112, 236]
        bias_list = [15, 127, 1023, 16383, 262143]
        self.__length = force_length if force_length is not None else length_list[precision]
        self.__exponent = force_exponent if force_exponent is not None else exponent_list[precision]
        self.__mantissa = force_mantissa if force_mantissa is not None else mantissa_list[precision]
        self.__bias = force_bias if force_bias is not None else bias_list[precision]
        self.s = 0 if float(x) >= 0 else 1

        # if user enter an integer type. this code block turn string x integer to float type
        if(x.find('.') == -1):
            x = x + '.0'
       
        x = self.strAbs(x)
        self.x = x
        self.i = self.integer2binary(self.strTakeIntegerPart(x))

        #Write it as a string with a '0.' at the beginning of the decimal part for turn that type as a flat
        dotIndex = x.find('.')
        decimalPart = '0.' + x[dotIndex+1::]
        self.d = self.decimal2binary(decimalPart)

        self.e = self.integer2binary(str((self.i.size - 1) + self.__bias))
        self.m = np.append(self.i[1::], self.d)
        self.h = ''

    def __str__(self):
        r = np.zeros(self.__length, dtype=int)
        i_d = np.append(self.i[1::], self.d)
        r[0] = self.s
        r[1 + (self.__exponent - self.e.size):(self.__exponent + 1):] = self.e
        r[(1 + self.__exponent):(1 + self.__exponent + i_d.size):] = i_d[0:self.__mantissa]
        s = np.array2string(r, separator='')
        return s[1:-1].replace("\n", "").replace(" ", "")

    #@staticmethod
    def integer2binary(self, x: str) -> np.ndarray:
        b = np.empty((0,), dtype=int)
        while float(x) > 1:
            if(self.x == '0.0'):
                b = np.append(b, np.array([0]))
            else:
                b = np.append(b, np.array([int(float(x ))% 2]))
            x = self.strDivideBy(str(x),2)
        if(self.x == '0.0'):
            b = np.append(b, np.array([0]))
        else:
            b = np.append(b, np.array([x]))
        
        b = b[::-1]
        return b

    def decimal2binary(self, x: str) -> np.ndarray:
        b = np.empty((0,), dtype=int)
        i = 0
        while float(x) > 0 and i < self.__mantissa:
            x = self.strmultiplyFloatAndinteger(x, '2')
            b = np.append(b, np.array([int(float(x))]))
            if (float(x) >= 1):
                x = '0.' + x[2::]
            i += 1
        return b

    def str2hex(self) -> str:
        s = str(self)
        for i in range(0, len(s), 4):
            ss = s[i:i + 4]
            si = 0
            for j in range(4):
                si += int(ss[j]) * (2 ** (3 - j))
            sh = hex(si)
            self.h += sh[2]
        return self.h.capitalize()

    def strAbs(self, x: str):
        #take the absolute value of the number and return it as a string
        temp = str(x[0])
        if( str(temp) == '-'):
            x = x[1::]
        
        return x
    
    def strTakeDecimalPart(self, x: str):
        #find dot index and rearrange string result with decimal part
        getDecimalVal = x.find(".")
        return x[getDecimalVal+1::]
    
    def strTakeIntegerPart(self, x: str):
        #find dot index and rearrange string result with integer part
        getDecimalVal = str(x).find(".")
        return x[0:getDecimalVal:]

    def multiply(self , num1: str, num2: str):

        len1 = len(num1)
        len2 = len(num2)
        if len1 == 0 or len2 == 0:
            return "0"
 
        # will keep the result number in vector in reverse order
        result = [0] * (len1 + len2)
     
        # Below two indexes are used to find positions in result.
        i_n1 = 0
        i_n2 = 0
 
        # Go from right to left in num1
        for i in range(len1 - 1, -1, -1):
            carry = 0
            n1 = ord(num1[i]) - 48
    
            # To shift position to left after every multiplication of a digit in num2
            i_n2 = 0
    
            # Go from right to left in num2
            for j in range(len2 - 1, -1, -1):
                
                # Take current digit of second number
                n2 = ord(num2[j]) - 48

                # Multiply with current digit of first number and add result to previously stored result at current position.
                summ = n1 * n2 + result[i_n1 + i_n2] + carry
    
                # Carry for next iteration
                carry = summ // 10
    
                # Store result
                result[i_n1 + i_n2] = summ % 10
    
                i_n2 += 1
    
            # store carry in next cell
            if (carry > 0):
                result[i_n1 + i_n2] += carry
    
            # To shift position to left after every multiplication of a digit in num1.
            i_n1 += 1
    
        # ignore '0's from the right
        i = len(result) - 1
        while (i >= 0 and result[i] == 0):
            i -= 1
    
        # If all were '0's - means either both or one of num1 or num2 were '0'
        if (i == -1):
            return "0"
    
        # generate the result string
        s = ""
        while (i >= 0):
            s += chr(result[i] + 48)
            i -= 1
    
        return s

    def strmultiplyFloatAndinteger(self, floatNum: str, intNum: str) -> str :
        totalNum = ''
        intPart = self.strTakeIntegerPart(floatNum)
        decimalPart = self.strTakeDecimalPart(floatNum)
        totalInt = self.multiply(intPart, intNum)
        totalDecimal = self.multiply(decimalPart, intNum)

        # add part of decimal that must be turn integer after multiply to integer part
        if ( len(totalDecimal) != len(decimalPart) ):
            totalInt = str(int(totalInt) + int(totalDecimal[0]))
            totalDecimal = totalDecimal[1::]
        
        # write float result represent as a string
        totalNum = str(totalInt + '.' + totalDecimal)
        return totalNum    


    def strDivideBy(self, number: str , divisor: int):
        
        # As result can be very large store it in string 
        ans = ""; 

     

        # Find prefix of number that is larger than divisor. 
        idx = 0; 
        mtemp = ord(number[idx]) - ord('0')
        while (mtemp < divisor):
            mtemp = (mtemp * 10 + ord(number[idx + 1]) - ord('0'))
            idx += 1

        idx += 1
 

        # Repeatedly divide divisor with temp. After every division, update temp to include one more digit. 
        while ((len(number)) > idx): 

            # Store result in answer i.e. temp / divisor 
            ans += chr(math.floor(mtemp // divisor) + ord('0'))

            # Take next digit of number
            mtemp = ((mtemp % divisor) * 10 + ord(number[idx]) - ord('0'))
            idx += 1
 

        ans += chr(math.floor(mtemp // divisor) + ord('0'))

        # If divisor is greater than number 
        if (len(ans) == 0): 
            return 0

        # else return ans 
        return ans


if __name__ == '__main__':
    # with default options (Double Precision)
    number = '13.375'
    a = IEEE754(number)
    # you should call the instance as a string
    print(str(a))
    print(f"{a}")
    # you can get the hexadecimal presentation like this
    print(a.str2hex())
    # or you can specify a precision and
    for p in range(5):
        a = IEEE754(number, p)
        print("x = %s | b = %s | h = %s" % (number, a, a.str2hex()))
    # or you can use your own custom precision
    a = IEEE754(number,
                force_length=19,
                force_exponent=6,
                force_mantissa=12,
                force_bias=31)
    print(f"{a}")
