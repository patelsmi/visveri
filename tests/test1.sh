source common.sh

GOLDEN="{'adder': {'inputs': ['add_inp1', 'add_inp2'], 'submodules': {}, 'outputs': ['add_out']}, 'wrapper': {'inputs': [], 'submodules': {'inst_adder': 'adder', 'inst_sub': 'sub'}, 'outputs': []}, 'sub': {'inputs': ['sub_inp1', 'sub_inp2'], 'submodules': {}, 'outputs': ['sub_out']}}"

TEST="$(python $SOURCE_DIR/parser.py -o /tmp/temp -top wrapper -i $EXP_DIR/adder.v $EXP_DIR/sub.v $EXP_DIR/wrapper.v)"


if [ "$GOLDEN" == "$TEST" ];then
    echo "Test Passed"
else
    echo "Test Failed"
    echo ""
    echo "Golden: $GOLDEN"
    echo ""
    echo "Output: $TEST"
fi


