package main

import (
	"fmt"
	"strconv"
)

// declare global variables
var intKey0, intKey1, intKey2 [4]int

//constant matrix used for mix column
var constantMatrix = [4]int{3, 2, 2, 3}

/*
	convert binary string to int
*/
func string_to_int(block [4]string) [4]int {
	res := [4]int{}
	for i, nibble := range block {
		temp, err := strconv.ParseUint(nibble, 2, 0)
		if err == nil {
			res[i] = int(temp)
		}
	}
	return res
}

/*
	convert int to binary string
*/
func int_to_string(block [4]int) [4]string {
	res := [4]string{}
	for i, nibble := range block {
		temp := strconv.FormatInt(int64(nibble), 2)
		for j := len(temp); j < 4; j++ {
			temp = "0" + temp

		}
		res[i] = temp
	}
	return res
}

/*
nibble sub process in encryption
*/
func nibble_sub(block [4]string) [4]string {
	var replace [4]string
	for i, value := range block {
		replace[i] = nibble_sub_helper(value)
	}
	return replace
}

/*
nibble sub helper
*/
func nibble_sub_helper(value string) string {
	var output string
	if value == "0000" {
		output = "1110"
	} else if value == "0001" {
		output = "0100"
	} else if value == "0010" {
		output = "1101"
	} else if value == "0011" {
		output = "0001"
	} else if value == "0100" {
		output = "0010"
	} else if value == "0101" {
		output = "1111"
	} else if value == "0110" {
		output = "1011"
	} else if value == "0111" {
		output = "1000"
	} else if value == "1000" {
		output = "0011"
	} else if value == "1001" {
		output = "1010"
	} else if value == "1010" {
		output = "0110"
	} else if value == "1011" {
		output = "1100"
	} else if value == "1100" {
		output = "0101"
	} else if value == "1101" {
		output = "1001"
	} else if value == "1110" {
		output = "0000"
	} else if value == "1111" {
		output = "0111"
	}
	return output
}

/*
shift row operation in encryption
*/
func shift_row(block [4]string) [4]string {
	temp := block[1]
	block[1] = block[3]
	block[3] = temp
	return block
}

/*
Galois field operations
*/
func gf_mul(a int, b int) int {
	res := 0
	for i := 0; i < 4; i++ {
		if b&1 != 0 {
			res ^= a
		}
		hi_bit_set := a & 8
		a <<= 1
		if hi_bit_set == 8 {
			a ^= 19
		}
		b >>= 1
	}
	return res
}

/*
mix column in encryption
*/
func mix_column(block [4]string, constant_matrix [4]int) [4]int {
	new_block := [4]int{}
	update := [4]int{}
	for i, nibble := range block {
		temp, err := strconv.ParseInt(nibble, 2, 0)
		if err == nil {
			new_block[i] = int(temp)
		}
	}
	update[0] = gf_mul(new_block[0], constant_matrix[0]) ^ gf_mul(new_block[1], constant_matrix[2])
	update[1] = gf_mul(new_block[0], constant_matrix[1]) ^ gf_mul(new_block[1], constant_matrix[3])
	update[2] = gf_mul(new_block[2], constant_matrix[0]) ^ gf_mul(new_block[3], constant_matrix[2])
	update[3] = gf_mul(new_block[2], constant_matrix[1]) ^ gf_mul(new_block[3], constant_matrix[3])
	return update
}

func key_addition(block [4]int, key [4]int) [4]int {
	res := [4]int{}
	for i := 0; i < 4; i++ {
		res[i] = key[i] ^ block[i]
	}
	return res
}

func produce_key(original_key [4]int, key_round int) [4]int {
	res := [4]int{}

	temp_nibble_sub := strconv.FormatInt(int64(original_key[3]), 2)
	for j := len(temp_nibble_sub); j < 4; j++ {
		temp_nibble_sub = "0" + temp_nibble_sub
	}

	replace := nibble_sub_helper(temp_nibble_sub)
	new_replace, err := strconv.ParseInt(replace, 2, 0)
	if err == nil {
		res[0] = original_key[0] ^ int(new_replace) ^ key_round
	}
	res[1] = res[0] ^ original_key[1]
	res[2] = res[1] ^ original_key[2]
	res[3] = res[2] ^ original_key[3]

	return res
}

//encryption process of mini-AES
func encryption() [4]int {
	//Here is the block of 4 nibbles
	s := [4]string{"1001", "1100", "0110", "0011"}
	fmt.Print("This is the input block: ")
	fmt.Println(s)

	//produce the keys
	key0 := [4]string{"1100", "0011", "1111", "0000"}
	intKey0 = string_to_int(key0)
	fmt.Print("This is the key in the round 0: ")
	fmt.Println(int_to_string(intKey0))
	intKey1 = produce_key(intKey0, 1)
	fmt.Print("This is the key in the round 1: ")
	fmt.Println(int_to_string(intKey1))
	intKey2 = produce_key(intKey1, 2)
	fmt.Print("This is the key in the round 2: ")
	fmt.Println(int_to_string(intKey2))

	//At first do key addition with plaintext and first key
	newS := key_addition(string_to_int(s), intKey0)
	fmt.Print("This is the result of first key addition in the encryption: ")
	fmt.Println(int_to_string(newS))

	//round 1
	step1 := nibble_sub(int_to_string(newS))
	fmt.Print("This is the result of nibble sub in the first round: ")
	fmt.Println(step1)
	step2 := shift_row(step1)
	fmt.Print("This is the result of shift row in the first round: ")
	fmt.Println(step2)
	step3 := mix_column(step2, constantMatrix)
	fmt.Print("This is the result of mix column in the first round: ")
	fmt.Println(int_to_string(step3))
	step4 := key_addition(step3, intKey1)
	fmt.Print("This is the result of key addition in the first round: ")
	fmt.Println(int_to_string(step4))

	//round 2
	step1Round2 := nibble_sub(int_to_string(step4))
	fmt.Print("This is the result of nibble sub in the second round: ")
	fmt.Println(step1Round2)
	step2Round2 := shift_row(step1Round2)
	fmt.Print("This is the result of shift row in the second round: ")
	fmt.Println(step2Round2)
	step3Round2 := key_addition(string_to_int(step2Round2), intKey2)

	fmt.Print("Final ciphertext is ")
	fmt.Println(int_to_string(step3Round2))
	return step3Round2
}

func inverse_nibble_sub(block [4]string) [4]string {
	res := [4]string{}
	var nibble_sub_table = [16]string{"1110", "0011", "0100", "1000", "0001", "1100", "1010", "1111", "0111", "1101", "1001", "0110", "1011", "0010", "0000", "0101"}
	for i, value := range string_to_int(block) {
		res[i] = nibble_sub_table[value]
	}
	return res
}

func decryption(ciphertext [4]int) {
	//decrypt round
	step1 := key_addition(ciphertext, intKey2)

	step2 := shift_row(int_to_string(step1))

	step3 := inverse_nibble_sub(step2)

	step4 := key_addition(string_to_int(step3), intKey1)

	step5 := mix_column(int_to_string(step4), constantMatrix)

	step6 := shift_row(int_to_string(step5))

	step7 := inverse_nibble_sub(step6)
	fmt.Print("This is the inverse of nibble sub in decryption: ")
	fmt.Println(step7)

	step8 := key_addition(string_to_int(step7), intKey0)

	fmt.Print("Original plaintext is ")
	fmt.Println(int_to_string(step8))

}

func main() {
	decryption(encryption())
}
